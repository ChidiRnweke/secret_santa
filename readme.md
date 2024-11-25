# Secret Santa

Everyone loves a good Secret Santa, but it can be a pain to organize. This app makes it easy to set up a Secret Santa exchange, and even easier to draw names.

## But why?

The app was mostly an excuse to play with some new tech. I used it to add a few things to my toolbox:

- [Infisical](https://infisical.com) open source secrets management, to graduate from what I was doing before.
- [OpenTelemetry](https://opentelemetry.io/) for observability. I'm using:
  - [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) to collect traces and metrics to send to:
    - [Loki](https://grafana.com/oss/loki/) to store logs. The data resides in a [MinIO](https://min.io/) bucket.
    - [Prometheus](https://prometheus.io/) to store metrics.
  - [Grafana](https://grafana.com/) the previous two tools are great, but Grafana is the best tool to visualize them.

As usual, the infrastructure is managed with [Ansible](https://www.ansible.com/), and the CI/CD is done with [GitHub Actions](https://github.com/features/actions).

For the frontend I started with Vue.js as opposed to my usual sveltekit. I wanted to try something new, and I'm happy with the results. Like always I'm using [Vite](https://vitejs.dev/) as the build tool, and [Tailwind CSS](https://tailwindcss.com/) for the styles.