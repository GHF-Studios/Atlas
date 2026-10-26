#!/usr/bin/env python3
"""Read-only reproduction of issue #1 rebase integration failures.
Builds a headless executable in a temporary directory, using the checkout's
unchanged canonical-position, layer, and rebase modules. No test suite, GUI,
repository edits, commits, or push. Optional --publish updates issue #1 after
the diagnostic succeeds. Requires cached Cargo deps and gh for publishing.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

EXPECTED = {'spacetime-engine/src/spatial/mod.rs': '8460592a5c8cdd14855d263f70f03f73b1f0c8014ea32e4056a3fdcab0a47b39', 'spacetime-engine/src/spatial/rebase/mod.rs': 'fbb1a794e045988cb506a65fea2818fd2a10927f65d08afa7e5235ace626161b', 'spacetime-engine/src/spatial/position/mod.rs': '15f50fee8506b006e5fa5d2199eb048888cc47547913a96a3fc31c35d4b58a69', 'spacetime-engine/src/spatial/position/chunk_address/mod.rs': 'c161b9821e00ffe82228c36d9bf015ac7bee2ec3e6f6705f5c6054b9035a1068', 'spacetime-engine/src/spatial/layer/mod.rs': '5653599aacb64f0926882979052810db52ab6dd5b1bfd383db705d6c481d7b5f', 'Cargo.lock': '198c6c23f35cff116c99edffad5effeb49e0035de016e5b6e9ff2231ea70b1d4'}
MAIN = 'use bevy::{ecs::system::RunSystemOnce, prelude::*};\nuse avian3d::prelude::*;\n\nfn inspect(query: SpatialQuery, poses: Query<(&Position, &ColliderAabb), With<Floor>>) {\n    let position = poses.single().unwrap();\n    println!("position={:?} collider_aabb={:?}",position.0.0,position.1);\n    for x in [256.0, 0.0] {\n        println!("downward query at x={x}: {:?}", query.cast_ray(Vec3::new(x,2.0,0.0),Dir3::NEG_Y,10.0,true,&SpatialQueryFilter::default()).map(|hit|hit.distance));\n    }\n}\n\n\n#[allow(dead_code, unused_imports)] mod spatial;\nuse spatial::*;\n#[derive(Component)] struct Floor;\nfn main(){\n let repair=std::env::args().any(|s|s=="--refresh");\n let mut app=App::new();\n app.add_plugins((MinimalPlugins, TransformPlugin, PhysicsPlugins::default()));\n app.insert_resource(Gravity::ZERO);\n app.insert_resource(spatial::initial_frame());\n app.insert_resource(bevy::time::TimeUpdateStrategy::ManualDuration(std::time::Duration::from_secs_f64(1.0/60.0)));\n spatial::configure(&mut app);\n if repair {app.add_systems(PostUpdate,avian3d::collider_tree::update_moved_collider_aabbs::<Collider>.after(bevy::transform::TransformSystems::Propagate));}\n app.finish();app.cleanup();\n app.world_mut().spawn((Floor,UsfScaleLayer::new(SpatialScale::ZERO),RigidBody::Static,Collider::cuboid(10.0,1.0,10.0),Transform::from_xyz(256.0,0.0,0.0)));\n let anchor=app.world_mut().spawn((UsfSpatialAnchor,UsfLogicalProjection,UsfScaleLayer::new(SpatialScale::ZERO),Transform::from_xyz(255.9,2.0,0.0))).id();\n let passive=app.world_mut().spawn((UsfScaleLayer::new(SpatialScale::new(1).unwrap()),Transform::from_xyz(10.0,0.0,0.0))).id();\n for _ in 0..4 {app.update();}\n println!("BEFORE REBASE (refresh={repair})");app.world_mut().run_system_once(inspect).unwrap();\n app.world_mut().get_mut::<Transform>(anchor).unwrap().translation.x=256.1;\n app.update();\n println!("AFTER PRODUCTION REBASE");app.world_mut().run_system_once(inspect).unwrap();\n let frame=app.world().resource::<UsfSpatialFrame>();\n let local=app.world().get::<Transform>(passive).unwrap().translation;\n let canonical=frame.origin().translated_at_scale(SpatialScale::new(1).unwrap(),local).unwrap();\n println!("passive S1 canonical X: before=100m after={}m; local X stays={}",canonical.relative_at_scale_bounded(&UsfPosition::zero(SpatialScale::ZERO),SpatialScale::ZERO,1000.0).unwrap().x,local.x);\n app.update();\n println!("AFTER NEXT FRAME / FIXED PHYSICS");app.world_mut().run_system_once(inspect).unwrap();\n}\n'
MANIFEST = '[package]\nname = "loo-rebase-probe"\nversion = "0.1.0"\nedition = "2024"\n[dependencies]\nbevy = { version = "=0.19.1", default-features = false, features = ["std", "bevy_log"] }\navian3d = { version = "=0.7.0", default-features = false, features = ["3d", "f32", "parry-f32"] }\n[profile.dev]\ndebug = 0\n'

ISSUE_UPDATE = {'expected_body': '## Intent\nDiagnose and stabilize the coherence boundary between canonical celestial reality and its disposable runtime representations: runtime charts, scale-local voxel realization, collision, coverage/readiness, and presentation.\n\nEarth is the semantic/default thing. A chart rebase, scale-local realization transition, missing coverage, or presentation fallback must not silently substitute a different world surface.\n\n## Why\nConcrete runtime evidence shows a reversible **256 m-aligned** discontinuity around Earth\'s surface:\n\n- above about **AGL +256 m**, the unintended white floor disappears and Earth appears;\n- below about **AGL 0 m**, Earth disappears and the unintended white floor appears;\n- continuing below about **AGL -256 m**, the white floor disappears;\n- reversing direction reproduces the cycle: white floor around **0 m**, Earth again around **+256 m**.\n\nThe white floor is not intentional and must not become supported fallback behavior.\n\nThis spacing now has a specific code-level correlate: current spatial code defines both\n\n- `REBASE_THRESHOLD_NATIVE = 256.0`\n- `REBASE_QUANTUM_NATIVE = 256.0`\n\nand `rebase_local_frame` shifts the bounded runtime chart in multiples of that quantum.\n\nThat exact numerical alignment makes the runtime chart/rebase boundary a **leading suspect**. It still does not prove that rebasing itself is wrong: the fault may be a consumer conflating runtime-local chart coordinates with semantic identity, realization ownership, coverage, presentation, collision, or cached local-space state.\n\n## Current truth\nCurrent code already states the intended boundaries:\n\n- `game/world/procedural/scenery` does **not** create generic "terrain everywhere" fallback; matter/presentation/physics realizers must attach to actual semantic authority.\n- `spatial/view` says a local terrain patch must never globally hide its ancestral whole-body presentation.\n- `voxel/realization` says scale participation is representation policy rather than semantic body identity, and absence of refinement must never erase local reality.\n- voxel render/collision manifestations are disposable realizations derived from authoritative state.\n- `spatial/rebase` changes the bounded numerical chart while preserving canonical position; it updates same-scale runtime transforms/physics positions, updates scale-layer frames, and publishes `UsfOriginRebased`.\n\nThe observed Earth/white-floor switching means some runtime path is violating those contracts.\n\n## Decisions\n- The white floor is unintended. Do not preserve it, legitimize it as fallback terrain, or design around it.\n- Earth remains the semantic/default celestial object across chart, scale, residency, coverage, and presentation transitions.\n- Treat the exact 256 alignment as evidence that floating-origin/chart rebasing is involved in the trigger path until disproven.\n- Do **not** reduce that to "the rebase constants are wrong." A 256-unit rebase may be perfectly valid while another subsystem incorrectly lets numerical chart state choose semantic/realization ownership.\n- The leading architectural suspicion is therefore **conflation between bounded runtime-chart representation and semantic/realization state**.\n- Diagnose ownership boundaries before implementing a visible patch. Fixing only one threshold without explaining the repeated reversible pattern is insufficient.\n- Coarse/ancestral celestial context and finer bounded refinement must compose; refinement must not globally replace Earth with an unrelated surface.\n\n## Open questions\n- Which state changes exactly when the spatial anchor crosses a 256-unit rebase boundary?\n- What entity/realizer actually produces the white floor?\n- Which rebase consumers or local-space caches fail to preserve semantic/realization coherence?\n- Does rebase indirectly alter voxel demand/residency, manifestation membership/retirement, coverage publication, presentation visibility, or collision ownership?\n- Is the symptom presentation-only, or do collision/query/edit semantics switch with the visible surface as well?\n- Does the cycle continue at additional 256-unit crossings in an otherwise equivalent local setup?\n\n## Relations\nBlocks #5, #6, and #12.\n\nRelates to:\n- #19 — semantic identity vs authority partitions/logical realizations/presentation;\n- #20 — continuous mesh/collider refinement across the scale stack;\n- #26 — worldgen construction/recovery of durable semantic objects rather than bespoke scenery identity.\n\nThose issues describe broader foundations or follow-on work. This issue owns diagnosis of this concrete 256-aligned runtime incoherence. Do not move implementation into the broader issues until evidence identifies the violated ownership boundary.\n\n## Done when\n- The exact state transition triggered at the 256-unit boundaries is identified with runtime/code evidence.\n- The producing mechanism behind the white floor is identified.\n- The unintended white floor is gone rather than merely hidden at one boundary.\n- Earth remains coherent through repeated rebases/crossings in both directions.\n- Presentation, collision, realization residency, and published coverage agree about the same celestial reality.\n- Any broader architectural conflation discovered here is distilled into the relevant existing foundation issue instead of being left as an isolated visual patch.\n', 'desired_body': "## Intent\nDiagnose and stabilize the coherence boundary between canonical celestial reality and its disposable runtime representations: runtime charts, scale-local voxel realization, collision, coverage/readiness, and presentation.\n\nEarth is the semantic/default thing. A chart rebase, scale-local realization transition, missing coverage, or presentation fallback must not silently substitute a different world surface.\n\n## Why\nThe original runtime report described a reversible **256 m-aligned** discontinuity around Earth's surface:\n\n- above about **AGL +256 m**, the unintended white floor disappears and Earth appears;\n- below about **AGL 0 m**, Earth disappears and the unintended white floor appears;\n- continuing below about **AGL -256 m**, the white floor disappears;\n- reversing direction reproduces the cycle: white floor around **0 m**, Earth again around **+256 m**.\n\nThe white floor is not intentional and must not become supported fallback behavior.\n\nThis spacing now has a specific code-level correlate: current spatial code defines both\n\n- `REBASE_THRESHOLD_NATIVE = 256.0`\n- `REBASE_QUANTUM_NATIVE = 256.0`\n\nand `rebase_local_frame` shifts the bounded runtime chart in multiples of that quantum.\n\nThat numerical alignment led to the rebase investigation. Specific rebase integration failures are now reproduced, while their complete causal link to the visible surface switching remains unresolved.\n\n## Current truth\nInvestigated at [e14e928](https://github.com/GHF-Studios/Loo-Cast/commit/e14e928a1f4870a60c937009629ee4490b717437). The previous fixture/canonical-coordinate tranche did **not** resolve the reported displacement: the surface is now gray; its producer may be Earth itself. The exact ±256 m switching has not been rechecked in the latest build.\n\n- Authored celestial construction now lives in `game/world/fixture`; the procedural bootstrap and duplicate scale-layer frame resource were removed.\n- The rebase updates one shared canonical origin but shifts only active-scale/layerless runtime transforms and physics positions. An unchanged S1 position at native X=10 is consequently interpreted as 356 m instead of 100 m after an S0 +256 rebase. This is a reproduced coordinate-contract failure.\n- Collision bounds do not move with the rebased physics pose until the next fixed physics update. A headless reproduction moves a floor from X=256 to X=0; its bounds stay near 256 and a query at the new location misses. Refreshing Avian's moved-collider bounds in PostUpdate restores the immediate hit.\n- The 256 policy originated in an explicitly fixed-S0 prototype (`324fea3`). Canonical USF addressing uses 10 children per axis and 1000 native units per chunk. A 100-unit diagnostic counterfactual reproduces both failures at the new boundary.\n- `UsfOriginRebased` publishes a bare vector without its scale; portal caches apply it indiscriminately across travelers.\n- Voxel manifestations and far scenery also reproject from canonical state. Therefore the reproduced rebase defects do **not** yet establish the complete visual trigger or the gray surface's producer.\n\nThese results came from a headless runtime diagnostic using unchanged production rebase/position/layer modules and locked dependencies. No test suite was run. No production fix was applied in this reinvestigation; the mesh-refinement draft is parked.\n\n## Decisions\n- The white floor is unintended. Do not preserve it, legitimize it as fallback terrain, or design around it.\n- Earth remains the semantic/default celestial object across chart, scale, residency, coverage, and presentation transitions.\n- Treat the exact 256 alignment as evidence that floating-origin/chart rebasing is involved in the trigger path until disproven.\n- Leslie wants chart policy aligned with the decimal USF model. Changing 256 to 100 alone is insufficient: the diagnostic reproduces the same integration faults at the new boundary.\n- A chart change must preserve canonical positions and update affected runtime representations in their own units, with dependent caches coherent before consumers observe the new frame. Explicit chart ownership and publication ordering are the repair boundary.\n- Diagnose ownership boundaries before implementing a visible patch. Fixing only one threshold without explaining the repeated reversible pattern is insufficient.\n- Coarse/ancestral celestial context and finer bounded refinement must compose; refinement must not globally replace Earth with an unrelated surface.\n\n## Open questions\n- Which of the reproduced rebase integration faults participates in the reported visual switching, and what else changes at that boundary?\n- What entity/realizer produces the displaced white/gray surface? Is it Earth's own representation?\n- What chart ownership should each scale-local manifestation and cache carry, and which additional consumers need coordinated updates?\n- Does rebase indirectly alter voxel demand/residency, manifestation membership/retirement, coverage publication, presentation visibility, or collision ownership?\n- Is the symptom presentation-only, or do collision/query/edit semantics switch with the visible surface as well?\n- Does the cycle continue at additional 256-unit crossings in an otherwise equivalent local setup?\n\n## Relations\nBlocks #5, #6, and #12.\n\nRelates to:\n- #19 — semantic identity vs authority partitions/logical realizations/presentation;\n- #20 — continuous mesh/collider refinement across the scale stack;\n- #26 — worldgen construction/recovery of durable semantic objects rather than bespoke scenery identity.\n\nThose issues describe broader foundations or follow-on work. This issue owns diagnosis of this concrete 256-aligned runtime incoherence. Do not move implementation into the broader issues until evidence identifies the violated ownership boundary.\n\n## Done when\n- The exact state transition triggered at the 256-unit boundaries is identified with runtime/code evidence.\n- The producing mechanism behind the white floor is identified.\n- The unintended white floor is gone rather than merely hidden at one boundary.\n- Earth remains coherent through repeated rebases/crossings in both directions.\n- Presentation, collision, realization residency, and published coverage agree about the same celestial reality.\n- Any broader architectural conflation discovered here is distilled into the relevant existing foundation issue instead of being left as an isolated visual patch.\n", 'comment': "<!-- loo-cast-issue1-rebase-evidence-e14e928-v1 -->\nReinvestigation at [e14e928](https://github.com/GHF-Studios/Loo-Cast/commit/e14e928a1f4870a60c937009629ee4490b717437): the previous tranche did **not** resolve the reported surface displacement. Leslie reports the surface is now gray; the exact ±256 m crossings have not been rechecked. The apparent floor may be displaced Earth itself, so its producing representation remains unconfirmed.\n\nTwo rebase integration faults are now reproduced in a headless executable using the checkout's unchanged canonical-position, scale-layer, and rebase modules, with its locked Bevy 0.19.1 / Avian 0.7 dependencies. This was runtime diagnosis, not a test-suite run.\n\n1. **A shared origin changes while another scale keeps old coordinates.** With an S0 anchor crossing 256, an S1 object at native X=10 retains that transform. Interpreting it through the shared frame changes its canonical X from 100 m to 356 m. `rebase_local_frame` updates the shared origin but shifts only active-scale/layerless transforms and physics positions. Gravity/navigation and other consumers interpret scale-local coordinates through that shared origin. This violates the coordinate contract; it does not establish that every canonical entity is directly mutated.\n2. **Collision bounds lag behind the rebased physics pose.** A static floor moves from X=256 to X=0, while its collision bounds remain [250.995, 261.005]. A downward query at its new location misses. After the next fixed physics update, bounds become [-5.005, 5.005] and the query hits again at distance 1.5. Character queries run in FixedUpdate, before the following FixedPostUpdate refresh. An experimental PostUpdate call to Avian's moved-collider bounds updater restores the immediate hit. This confirms a temporary cache inconsistency, not permanent collider disappearance.\n\n**256 is a legacy policy, not the USF chunk size.** Commit `324fea3` introduced it in an explicitly fixed-S0 prototype; later multiscale work retained it. Canonical addressing is decimal (10 children per axis, 1000 native units per chunk). Changing only the throwaway diagnostic's threshold/quantum to 100 reproduced both failures at 100: the passive object's interpreted position became 200 m, and the collision query still missed until physics refreshed. Decimal chart policy is Leslie's intended direction; changing the constant alone is insufficient.\n\nThere are further integration warning signs: `UsfOriginRebased` carries a bare shift without its scale, and portal caches apply that same vector to every traveler. These need chart/units ownership, not another appearance patch. The appropriate repair boundary is a coherent chart change: preserve canonical positions, update each affected runtime representation in its own units, and refresh dependent caches before consumers observe the new frame. This directly informs #19.\n\n**Limits:** voxel manifestations and far scenery have canonical reprojection paths, so the two reproduced failures do not yet identify the gray surface's producer or prove the complete visual trigger chain. The mesh-refinement draft is parked. Production remains unchanged in this reinvestigation; no new commit/push or full-fix claim. The checkout is currently read-only. #1 remains OPEN / ACTIVE.", 'marker': '<!-- loo-cast-issue1-rebase-evidence-e14e928-v1 -->'}

def github_json(gh, endpoint, payload=None):
    command = [gh, "api", endpoint]
    data = None
    if payload is not None:
        method, body = payload
        command += ["--method", method, "--input", "-"]
        data = json.dumps(body)
    result = subprocess.run(command, input=data, text=True, capture_output=True)
    if result.returncode:
        raise SystemExit("GitHub operation failed. Local source is untouched. "
                         "If a write response was interrupted, rerun: the issue snapshot "
                         "and comment marker are checked before writes.\n" + result.stderr)
    return json.loads(result.stdout)

def issue_snapshot(gh):
    endpoint = "repos/GHF-Studios/Loo-Cast/issues/1"
    issue = github_json(gh, endpoint)
    if issue["state"] != "open" or "ACTIVE" not in [label["name"] for label in issue["labels"]]:
        raise SystemExit("Issue state/workflow changed; inspect it before publishing. No write attempted.")
    if issue["body"] not in (ISSUE_UPDATE["expected_body"], ISSUE_UPDATE["desired_body"]):
        raise SystemExit("Issue body changed; preserve the new information and reconcile this tranche. No write attempted.")
    comments = []
    page = 1
    while True:
        batch = github_json(gh, f"{endpoint}/comments?per_page=100&page={page}")
        comments.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    matches = [item for item in comments if ISSUE_UPDATE["marker"] in item["body"]]
    if len(matches) > 1 or any(item["body"] != ISSUE_UPDATE["comment"] for item in matches):
        raise SystemExit("Evidence comment was edited or duplicated; inspect before publishing. No write attempted.")
    return issue, matches

def publish_evidence(gh):
    # Refetch after the build. Never overwrite intervening issue decisions.
    issue, matches = issue_snapshot(gh)
    endpoint = "repos/GHF-Studios/Loo-Cast/issues/1"
    if issue["body"] != ISSUE_UPDATE["desired_body"]:
        github_json(gh, endpoint, ("PATCH", {"body": ISSUE_UPDATE["desired_body"]}))
    if not matches:
        github_json(gh, endpoint + "/comments", ("POST", {"body": ISSUE_UPDATE["comment"]}))
    issue, matches = issue_snapshot(gh)
    if issue["body"] != ISSUE_UPDATE["desired_body"] or len(matches) != 1:
        raise SystemExit("GitHub verification did not confirm both writes; rerun after inspecting the issue.")
    print("Evidence published: " + matches[0]["html_url"])

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.home() / "Vapor/Loo-Cast")
    parser.add_argument("--target-dir", type=Path, help="Optional existing Cargo build cache")
    parser.add_argument("--publish", action="store_true", help="After diagnosis, update issue #1 and add the guarded evidence comment")
    args = parser.parse_args()
    repo = args.repo.resolve()
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if head != "e14e928a1f4870a60c937009629ee4490b717437":
        raise SystemExit("Checkout HEAD changed; review this diagnostic before adapting it.")
    for relative, expected in EXPECTED.items():
        path = repo / relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise SystemExit(f"Source guard failed: {path}. This diagnostic targets e14e928; review it before adapting to changed code.")
    cargo = shutil.which("cargo")
    if not cargo:
        raise SystemExit("cargo is required")
    gh = shutil.which("gh") if args.publish else None
    if args.publish:
        if not gh:
            raise SystemExit("gh is required for --publish; omit the flag for local diagnosis only.")
        issue_snapshot(gh)
    work = Path(tempfile.mkdtemp(prefix="loo-cast-rebase-evidence-"))
    (work / "src").mkdir()
    (work / "Cargo.toml").write_text(MANIFEST)
    shutil.copyfile(repo / "Cargo.lock", work / "Cargo.lock")
    source = (repo / "spacetime-engine/src/spatial/mod.rs").read_text()
    frame = source[source.index("const REBASE_THRESHOLD_NATIVE"):source.index("#[derive(SystemSet")]
    def module_path(relative):
        return json.dumps(str(repo / relative), ensure_ascii=False)
    spatial = "use bevy::prelude::*;\nuse avian3d::prelude::Position;\n"
    spatial += f'#[path = {module_path("spacetime-engine/src/spatial/position/mod.rs")}] mod position;\npub use position::*;\n'
    spatial += f'#[path = {module_path("spacetime-engine/src/spatial/layer/mod.rs")}] mod layer;\npub use layer::*;\n'
    spatial += "#[derive(Component)] pub struct UsfLogicalProjection;\n" + frame
    spatial += f'#[path = {module_path("spacetime-engine/src/spatial/rebase/mod.rs")}] mod rebase;\n'
    spatial += "pub fn initial_frame() -> UsfSpatialFrame {UsfSpatialFrame {origin:UsfPosition::zero(SpatialScale::ZERO),rebase_count:0,last_shift:Vec3::ZERO}}\n"
    spatial += "pub fn configure(app: &mut App) {app.add_message::<UsfOriginRebased>().add_systems(PostUpdate,rebase::rebase_local_frame.before(bevy::transform::TransformSystems::Propagate));}\n"
    env = os.environ.copy()
    if args.target_dir:
        env["CARGO_TARGET_DIR"] = str(args.target_dir.resolve())
    (work / "metadata.json").write_text(json.dumps({"repo":str(repo),"head":subprocess.check_output(["git","-C",str(repo),"rev-parse","HEAD"],text=True).strip(),"source_sha256":EXPECTED},indent=2))
    for name, refresh, decimal in [("production",False,False),("refresh-experiment",True,False),("decimal-counterfactual",False,True)]:
        # Only the throwaway harness changes in the counterfactual.
        module = spatial.replace("= 256.0;", "= 100.0;") if decimal else spatial
        program = MAIN.replace("256.0","100.0").replace("255.9","99.9").replace("256.1","100.1") if decimal else MAIN
        (work / "src/spatial.rs").write_text(module)
        (work / "src/main.rs").write_text(program)
        command = [cargo,"run","--manifest-path",str(work / "Cargo.toml"),"--offline","--quiet"]
        if refresh:
            command += ["--","--refresh"]
        print(f"Running {name}...", flush=True)
        result = subprocess.run(command, env=env, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (work / f"{name}.log").write_text(result.stdout)
        print(result.stdout)
        if result.returncode:
            raise SystemExit(f"Diagnostic failed; logs retained at {work}")
    print(f"Evidence saved at {work}; checkout untouched.")
    if args.publish:
        publish_evidence(gh)

if __name__ == "__main__":
    main()
