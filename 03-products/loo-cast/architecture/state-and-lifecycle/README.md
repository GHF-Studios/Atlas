# State and Lifecycle

- Source workspaces and manifests live in Git checkout
- Package command builds selected Packagepack and promotes target executable to managed `bin/<target>`
- Steam depot payload excludes Vapor Home/runtime state and source checkout
- In-game persistent-world/save lifecycle: not established by current workspace README