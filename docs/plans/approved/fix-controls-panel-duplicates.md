Task: Fix duplicate declarations and duplicate default export in react-frontend/src/components/ControlsPanel.jsx.

Scope: Modify only react-frontend/src/components/ControlsPanel.jsx.

Implementation:
1. Keep one set of state declarations for params, loading and error.
2. Keep one useEffect for loading effect parameters.
3. Keep one handleParamChange function.
4. Keep one default export.
5. Preserve existing controls, API endpoints and behavior.

Verification: Run the frontend production build and inspect the diff.

Do not modify App.jsx, CSS, Flask files, or unrelated files.