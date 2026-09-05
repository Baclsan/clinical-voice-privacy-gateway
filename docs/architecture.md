# Architecture

The gateway separates route selection, local privacy processing, deterministic verification, and external egress.

```text
input/audio
   |
   v
local speech-to-text
   |
   v
explicit route
   |---------------- NORMAL --------------------|
   |                                             v
   |                                      disclosure boundary
   |                                             |
   +--------------- CLINICAL                    v
                       |                     provider sink
                       v
               local privacy transform
                       |
                       v
                 candidate text
                       |
                       v
             deterministic verifier
                       |
                       v
               VerifiedSafeText
                       |
                       v
                disclosure boundary
                       |
                       v
                   provider sink
```

The public MVP intentionally does not implement speech recognition, model execution, messaging-platform integration, or a specific external AI provider.
