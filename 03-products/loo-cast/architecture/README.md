# Architecture

> **Status:** Draft — distinguish the composed product from its three content artifacts.

Describe how the Loo Cast experience is composed from Spacetime Engine, Loo Cast Game, and Loo Cast Packagepack, and how each artifact relates to Vapor. The workspace registers these as sibling projects; the Packagepack references the other two by Vapor identity and links them into the runnable executable.

Keep source implementation in the Loo-Cast workspace and engine code. This page explains the product boundary, not Cargo dependency details alone.
