# Legacy Azure SDK for Java Migration with AppMod — Video Script

> **Total runtime:** ~5 minutes | **Audience:** Internal engineering/PM
> **Format:** Slide narration (no live demo — narrate over screenshots)

---

## Slide 2 — Context (~1:00)

The new Azure SDK libraries have been generally available for over four years, and the older, legacy SDKs have been out of SLA since September 2023. Yet adoption of the new SDKs has been slow.

Take a look at this chart. Track 1 still accounts for a significant share of both requests and subscriptions. That's a real security concern.

And what's GitHub Copilot Modernization? What can it help with our scenario?
It is an agentic, end-to-end solution that provides approachable and consistent user experience for analyzing, upgrading, and migrating Java and .NET applications to Azure.
We're proposing a new capability that extends this extension to detect legacy Azure SDK dependencies - improving security, supportability, and latest Azure compatibility. Let me show you how it performs.

---

## Slide 3 — Benchmark Comparison (~1:15)

To validate this approach, Weidong ran benchmarks comparing several migration strategies across a set of test projects. Let's look at the two key metrics: build pass rate and CVE count.

On the left chart — build pass rate. A bare coding agent, without any modernization tooling, achieves only about 78%. Adding Azure Skills alone brings it to 76% — roughly the same, with a lot of variance run to run. By contrast, the Modernization extension reaches 96%. And our dedicated legacy-Azure-SDK upgrade skill(which is only a prototype) also hits 96%.

Now look at the right chart — CVE count, meaning known vulnerabilities remaining after migration. The plain agent and Azure Skills both leave about 5 CVEs unresolved. The Modernization extension eliminates all of them — zero CVEs. Our upgrade skill reduces them to just 1.

The takeaway is clear: Guided migration is both more reliable and more secure. A generic coding agent simply doesn't have the domain knowledge to handle Azure SDK migrations consistently.

---

## Slide 4 — Demo Walkthrough (~1:45)

Now let's walk through the actual user experience, using a real Java project as an example.

This project uses the legacy `azure-storage` library. It wanted to disable shared access key — also known as the infamous disable local auth  — for their storage account. But the legacy library doesn't support that capability. So they worked around it by mixing legacy and modern SDK usage in the same codebase. It's messy, and exactly the kind of technical debt we want to clean up.

Here's the workflow. In VS Code, you search the marketplace for "GitHub Copilot Modernization" and install the extension. On the left panel, you'll see the extension's quickstart menu.

Click "Start Assessment" to kick off a project assessment. The extension scans the project and generates an Assessment Report — that's what you see in the center panel. It identifies several issue categories. Our focus is the first one: "Legacy Azure SDKs for Java." As you can see, it detected legacy dependencies in `BlobStorageService.java`, `pom.xml`, and the test file. On the right is the detailed message — along with suggested actions.

Now, click "Run Task." This sends a structured instruction — developed by our team — to a custom agent that handles the actual migration. The agent generates a migration plan, executes each step, tracks progress, and produces a final summary.

It'll take some time and I'll let it run. Let's get directly into the result.

The migration plan includes project-specific guidelines selected by the agent from our instruction set, specifies upgrade goals, lists the technology stacks to replace, and lays out detailed migration steps. 

After execution, the summary reports on goal completion status, confirms minimum behavioral changes, and flags any CVEs it detects. The messy workaround for acquiring access tokens gets replaced cleanly with `DefaultAzureCredential` and the behavior remains the same.

---

## Slide 5 — Next Steps (~1:00)

Here's what's ahead for this work.

First, more validation and enhancement. We're working through all known legacy Track 1 data-plane SDKs to make sure we provide detailed migration guidance for each one. This is actively in progress.

Second, GHCP4A skill integration. We plan to ship a dedicated `legacy-azure-sdk-for-java-migration` skill that plugs directly into GitHub Copilot for Azure. We already have meetings set up with Kay to align on this, so the improvements we're building here will flow into that experience as well.

Stay tuned.

---

> **Word count:** ~740 | **Estimated read time:** ~4:55 at 150 wpm
