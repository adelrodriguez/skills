# Expose a service

Use this reference for browser previews, APIs, webhooks, and port forwarding.

## Locate the service and its audience

Determine whether the service runs inside Boat or on the local machine. Choose token-protected access, public access, or a private tunnel from the requested audience.

Use [services](services.md) to start a server that outlives the request. Verify the service inside the sandbox before exposing it. Serve only the intended application or artifact directory, not the entire home folder.

The step is done when the listening port, service location, and intended access are known.

## Expose a Boat port

For a server listening on `0.0.0.0`:

```sh
boat host "$id" 3000 --private
```

For a server listening only on loopback, add `--localhost`. The relay supports HTTP, WebSockets, and hot reload. Do not add it to a server already listening on `0.0.0.0`, because the relay can compete for the same port.

Boat publishes routes under `on.boat.dev`. A Vite preview may also need that host allowed. Use the narrow host configuration described in [how public URLs work](https://docs.boat.dev/hosting/how-it-works).

Token-protected access is the default. A full token URL grants access to whoever has it. Use `--public` only when the intended audience is public, and inspect the hosted directory and application first.

Verify the full external HTTPS request, not only `curl localhost`. A protected URL sets a cookie through a redirect, so an HTTP client must follow redirects and retain cookies. Keep token URLs out of logs and public PR evidence.

The step is done when the intended visitor can load the expected content and the access policy behaves as selected.

## Forward without publishing

To reach a Boat service from the local machine:

```sh
boat forward "$id" --remote 3000 --local 3000
```

To make a local service reachable from inside Boat:

```sh
boat forward "$id" --reverse --local 7777
```

The second command exposes the local port on loopback inside the sandbox. Use it only when that connection is part of the task. It does not inherit local browser logins or make the service public. Keep the SSH tunnel running while it is needed. It must be restarted after disconnection or sandbox resume.

See [SSH access](https://docs.boat.dev/ssh-access) for forwarding details. To publish a local service through Boat, the forwarding step and Boat-hosted route must both exist.

## Check the connection

- The internal service and external access path both work.
- The response is the intended application or artifact.
- Private access remains protected, or public access was intended.
- Retained servers and tunnels have an owner and a known lifetime.

Read [public URLs](https://docs.boat.dev/hosting) for route management and hiding a hosted port.
