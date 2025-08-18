# AudioVisualizerV2

This repository hosts a skeletal implementation of the **AudioVisualizerV2**
project.  The goal is to provide the structure and main classes described in
the project specification so further development can flesh out the details.

## Overview

* `audio.analyzer` – Generates or captures audio input and exposes FFT data.
* `midi.engine` – Minimal MIDI mapping engine emitting callbacks for actions.
* `visuals` – Base classes and a collection of placeholder presets.  Each
  preset declares its expected controls but leaves rendering unimplemented.
* `deck` – Associates a visual with audio analysis.
* `ui` – Simplified mixer and control panel widgets plus thumbnail utilities.
* `settings` – Persistence helpers for application and visual configuration.
* `main` – Entry point wiring all components together.

The code is intentionally lightweight and focuses on providing clear extension
points rather than production‑ready functionality.
