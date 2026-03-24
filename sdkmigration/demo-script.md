# Legacy Azure SDK for Java Migration with AppMod — Video Script

---

## Slide 2 — Context (~1:00)

The new Azure SDK libraries have been generally available for over four years. Yet adoption of the new SDKs has been slow.

According to our BI report, track 1 still accounts for a significant share of both requests and subscriptions.

And what is GitHub Copilot Modernization? What can it help with our scenario?
It is an agentic, end-to-end solution that provides approachable and consistent user experience for analyzing, upgrading, and migrating Java and .NET applications to Azure.
We're proposing a new capability that extends this extension to detect legacy Azure SDK dependencies - improving security, supportability, and latest Azure compatibility.

---

## Slide 3 — Benchmark Comparison (~1:15)

To validate this approach, Weidong ran benchmarks comparing several migration strategies across a set of test projects. From the two key metrics: build pass rate and CVE count, we can tell that guided migration is both more reliable and more secure. A generic coding agent simply doesn't have the domain knowledge to handle Azure SDK migrations consistently.
What's more, we experienced that bare coding agent would introduce new CVE during upgrade, while Modernization and our skill will not.

---

## Slide 4 — Demo Walkthrough (~1:45)

Now let's walk through the actual user experience, using a real Java project as an example.

This project has a mixed usage of Track1 and Track2 libraries to support disable local auth feature. This is exactly the kind of technical debt we want to clean up.

Here's the workflow. In VS Code marketplace, search for "GitHub Copilot Modernization" and install the extension. On the left panel, you'll see the extension's quickstart menu.

Click "Start Assessment" to kick off a project assessment. The extension scans the project and generates an Assessment Report — that's what you see in the center panel. It identifies several issue categories. Our focus be: "Legacy Azure SDKs for Java." As you can see, it detected legacy code and dependencies. On the right is the detailed message — along with suggested actions.

Now, click "Run Task." This sends a structured instruction — developed by our team — to a custom agent that handles the actual migration. The agent generates a migration plan, executes each step, tracks progress, and produces a final summary.

It'll take some time and I'll let it run. Let's get directly into the result.

The migration plan includes project-specific guidelines selected by the agent from our instruction set, specifies upgrade goals, lists the technology stacks to replace, and lays out detailed migration steps. 

After execution, the summary reports on goal completion status, confirms minimum behavioral changes, and flags any CVEs it detects. The messy workaround for acquiring access tokens gets replaced cleanly with `DefaultAzureCredential` and the behavior remains the same.

And that concludes the live demo part.

---

## Slide 5 — Next Steps (~1:00)

Here's what's ahead for this work.

First, more validation and enhancement. We're working through all known legacy Track 1 data-plane SDKs to make sure we provide detailed migration guidance for each one. This is actively in progress.

Second, GHCP4A skill integration. We plan to ship a dedicated `legacy-azure-sdk-for-java-migration` skill(mentioned in benchmark) that plugs directly into GitHub Copilot for Azure. We already have meetings set up with Kay to align on this, so the improvements we're building here will flow into that experience as well.

Stay tuned.

---

## Slide 6 — Appendix

For more detailed context and design documentation, I'll put links at the end in case you are interested.

That's all for the demo. Thank you!

---
