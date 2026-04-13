import type { Metadata } from "next";
import Image from "next/image";
import {
  ArrowRight,
  Database,
  MapPin,
  Search,
  Shield,
  Sparkles,
} from "lucide-react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNav } from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Job Openings",
  description: "Explore open roles and apply to Wenit Solutions opportunities.",
};

export default function JobsPage() {
  return (
    <div className="flex flex-1 flex-col">
      <SiteNav activeHref="/jobs" />

      <main className="mx-auto w-full max-w-screen-2xl px-6 pt-32 pb-24 md:px-12">
        <header className="mb-20 grid grid-cols-1 items-end gap-8 md:grid-cols-12">
          <div className="md:col-span-8">
            <div className="mb-4 flex items-center gap-4">
              <span className="text-xs font-bold uppercase tracking-widest text-secondary">
                2026 Hiring Trends
              </span>
              <div className="h-px w-12 bg-secondary/30" />
            </div>
            <h1 className="mb-6 text-5xl font-extrabold leading-[0.95] tracking-tighter text-on-surface md:text-7xl">
              Strategic <br />
              <span className="italic text-primary">Talent</span> Architecture
            </h1>
            <p className="max-w-xl text-lg font-light leading-relaxed text-on-surface-variant">
              We&apos;ve moved beyond resumes. Our frictionless, skills-first
              ecosystem connects architectural thinkers with high-precision
              engineering roles.
            </p>
          </div>

          <div className="md:col-span-4 md:flex md:flex-col md:items-end md:gap-6">
            <div className="w-full rounded-xl border-t border-primary/10 bg-surface-variant/60 p-6 backdrop-blur-2xl">
              <div className="mb-4 flex items-center justify-between">
                <span className="text-xs font-semibold uppercase tracking-widest text-on-surface-variant">
                  Active Pipeline
                </span>
                <span className="font-bold text-secondary">84%</span>
              </div>
              <div className="h-1 w-full overflow-hidden rounded-full bg-surface-container-highest">
                <div className="h-full w-[84%] bg-secondary" />
              </div>
              <p className="mt-3 text-[10px] uppercase tracking-tighter text-on-surface-variant/60">
                Competency-based matching active
              </p>
            </div>
          </div>
        </header>

        <section className="mb-12">
          <div className="flex flex-col items-center gap-2 rounded-full border-t border-primary/10 bg-surface-variant/60 p-2 backdrop-blur-2xl md:flex-row">
            <div className="flex w-full flex-1 items-center gap-3 px-6">
              <Search className="h-4 w-4 text-outline" />
              <input
                className="w-full bg-transparent font-light text-on-surface placeholder:text-outline/50 focus:outline-none"
                placeholder="Search roles by core competencies..."
                type="text"
              />
            </div>
            <div className="hidden h-8 w-px bg-outline-variant/30 md:block" />
            <div className="no-scrollbar flex gap-2 overflow-x-auto p-1">
              {[
                "Cloud Architecture",
                "Neural Systems",
                "Quantum Eng",
                "Remote Only",
              ].map((label) => (
                <button
                  key={label}
                  className={
                    label === "Remote Only"
                      ? "whitespace-nowrap rounded-full border border-secondary/20 bg-secondary-container/30 px-5 py-2 text-xs font-medium text-secondary"
                      : "whitespace-nowrap rounded-full bg-surface-container-highest px-5 py-2 text-xs font-medium text-primary transition-colors hover:bg-surface-bright"
                  }
                  type="button"
                >
                  {label}
                </button>
              ))}
            </div>
            <button
              className="rounded-full bg-[linear-gradient(135deg,#b9c7e4_0%,#0a192f_100%)] px-8 py-3 text-sm font-bold tracking-tight text-on-primary transition-transform hover:scale-95"
              type="button"
            >
              Find Matches
            </button>
          </div>
        </section>

        <section className="grid grid-cols-1 gap-6 md:grid-cols-12">
          <div className="group relative overflow-hidden rounded-xl bg-surface-container-low p-10 transition-all duration-500 hover:bg-surface-container-high md:col-span-8">
            <div className="absolute top-0 left-10 h-0.5 w-[30%] bg-secondary" />
            <div className="absolute top-10 right-10 flex gap-2">
              <span className="rounded border border-secondary/20 bg-secondary/10 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-secondary">
                High Priority
              </span>
            </div>
            <div className="flex h-full flex-col justify-between">
              <div>
                <div className="mb-6 flex items-center gap-3">
                  <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-surface-container-highest">
                    <Sparkles className="h-5 w-5 text-primary" />
                  </div>
                  <div>
                    <h3 className="text-2xl font-bold tracking-tight text-on-surface">
                      Principal Systems Architect
                    </h3>
                    <p className="text-sm text-on-surface-variant">
                      Full-time • Global Distributed
                    </p>
                  </div>
                </div>
                <p className="mb-8 max-w-2xl font-light leading-relaxed text-on-surface-variant">
                  Drive the foundational talent structures for our next-generation
                  neural workforce. This role requires deep competency in
                  organizational design and recursive system mapping.
                </p>
                <div className="mb-8 flex flex-wrap gap-2">
                  {["Rust", "Distributed Systems", "Game Theory"].map((tag) => (
                    <span
                      key={tag}
                      className="rounded-md bg-surface-container-highest px-4 py-1.5 text-xs text-on-surface-variant"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <div className="flex items-center justify-between border-t border-outline-variant/10 pt-6">
                <div className="flex flex-col">
                  <span className="text-[10px] uppercase tracking-widest text-outline">
                    Compensation
                  </span>
                  <span className="font-bold text-primary">
                    $240k — $310k + Equity
                  </span>
                </div>
                <button
                  className="rounded-md bg-primary px-8 py-3 text-sm font-bold text-on-primary transition-all hover:shadow-[0_0_20px_rgba(185,199,228,0.2)]"
                  type="button"
                >
                  Quick Apply
                </button>
              </div>
            </div>
          </div>

          <div className="relative rounded-xl border border-outline-variant/5 bg-surface-container-lowest p-8 transition-all hover:bg-surface-container md:col-span-4">
            <div className="mb-8">
              <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-surface-container">
                <Database className="h-5 w-5 text-secondary" />
              </div>
              <h3 className="mb-2 text-xl font-bold tracking-tight text-on-surface">
                Lead Data Synthesist
              </h3>
              <p className="text-xs font-bold uppercase tracking-widest text-on-surface-variant">
                Berlin / Hybrid
              </p>
            </div>
            <p className="mb-6 text-sm font-light leading-relaxed text-on-surface-variant">
              Translate complex behavioral data into actionable hiring archetypes
              for the 2026 landscape.
            </p>
            <div className="space-y-4">
              <div className="h-px w-full bg-outline-variant/20" />
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-primary">
                  Competency Focus
                </span>
                <span className="text-xs text-secondary">ETL • LLM Ops</span>
              </div>
              <button
                className="w-full rounded-md border border-primary/20 py-3 text-sm font-bold text-primary transition-colors hover:bg-primary/5"
                type="button"
              >
                Apply Now
              </button>
            </div>
          </div>

          <div className="group relative overflow-hidden rounded-xl bg-surface-container-low p-8 md:col-span-6">
            <div className="absolute top-0 left-8 h-0.5 w-[30%] bg-secondary" />
            <div className="flex items-start gap-6">
              <div className="hidden sm:block">
                <div className="relative h-16 w-16 overflow-hidden rounded-full border border-outline-variant/30">
                  <Image
                    className="h-full w-full object-cover grayscale opacity-60"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuBahc3N1eZSMHS5sW2VVICzbIqwsvCfDCphUOYtXC9eH1GDuTaGlBsarlbLmV6OdWjWDDa3JW8Fz9ztAYY0cjNiQLk8fP734GNT9sutTHMJSvvN9cAaShHOHxYLfPhyIQo8FRoWrFRDxc9nI_mvoXFqVamoFkc0fnhXnrevHJGdXjpUzq_maHv6mmoOziVxo1PEZqUhQ8AcdrfB9PeFWOwoTcXfHJtfXLsnnz3DXQGFzCcPqCmcnuMKCxTUx51iOd-crGcwKZSAdBU"
                    alt="Manager portrait"
                    fill
                    sizes="64px"
                  />
                </div>
              </div>
              <div className="flex-1">
                <span className="mb-2 block text-xs font-bold uppercase tracking-widest text-secondary-fixed-dim">
                  Manager Spotlight
                </span>
                <h3 className="mb-2 text-xl font-bold text-on-surface">
                  Senior Frontend Engineer
                </h3>
                <p className="mb-4 text-sm text-on-surface-variant">
                  &quot;We build interfaces that don&apos;t just display data,
                  they tell architectural stories.&quot;
                </p>
                <div className="flex items-center gap-4">
                  <span className="text-xs font-bold text-primary">
                    $180k — $220k
                  </span>
                  <button
                    className="text-xs font-bold uppercase tracking-widest text-secondary hover:underline"
                    type="button"
                  >
                    View Role
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between rounded-xl bg-[linear-gradient(135deg,#b9c7e4_0%,#0a192f_100%)] p-8 md:col-span-6">
            <div>
              <h4 className="mb-2 text-3xl font-extrabold tracking-tighter text-on-primary">
                92% Match Rate
              </h4>
              <p className="max-w-[240px] text-sm text-on-primary/70">
                Our skills-first engine reduces hiring friction by removing
                traditional resume bias.
              </p>
            </div>
            <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-4 border-white/10">
              <Shield className="h-10 w-10 text-on-primary" />
              <div className="absolute -top-1 -right-1 flex h-6 w-6 items-center justify-center rounded-full border-4 border-[#0a192f] bg-secondary">
                <span className="text-[12px] font-bold text-[#0a192f]">✓</span>
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-white/5 bg-surface-container-high p-8 md:col-span-4">
            <div className="mb-6 flex h-8 w-8 items-center justify-center rounded-md bg-secondary/10">
              <Shield className="h-4 w-4 text-secondary" />
            </div>
            <h3 className="mb-4 text-lg font-bold text-on-surface">
              Cyber-Physical Specialist
            </h3>
            <div className="mb-6 flex items-center gap-2">
              <MapPin className="h-3 w-3 text-outline" />
              <span className="text-xs text-on-surface-variant">
                Singapore / Remote
              </span>
            </div>
            <button
              className="w-full rounded-md bg-surface-container-highest py-2.5 text-xs font-bold text-on-surface transition-all hover:bg-surface-bright"
              type="button"
            >
              Quick View
            </button>
          </div>

          <div className="group rounded-xl border border-white/5 bg-surface-container-low p-8 transition-all hover:border-primary/20 md:col-span-4">
            <h3 className="mb-2 text-lg font-bold text-on-surface">
              Neural Ops Lead
            </h3>
            <p className="mb-6 text-xs text-on-surface-variant">
              Scale the backbone of our AI-integrated talent platforms.
            </p>
            <div className="mb-8 flex flex-wrap gap-2">
              {["PyTorch", "Kubernetes"].map((tag) => (
                <span
                  key={tag}
                  className="rounded bg-surface-container-lowest px-3 py-1 text-[10px] font-semibold uppercase text-outline"
                >
                  {tag}
                </span>
              ))}
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm font-bold text-secondary">$210k+</span>
              <ArrowRight className="h-4 w-4 text-primary transition-transform group-hover:translate-x-1" />
            </div>
          </div>

          <div className="relative min-h-[300px] overflow-hidden rounded-xl md:col-span-4">
            <Image
              className="h-full w-full object-cover grayscale brightness-50"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuC4pgf5bqOTcW9jg0jXODXMO9TZGPfOP-3ARZ59nGdAjk8FOU0inRBM_0G_b8mZnZT1SNMloszxQB31FQ-ATzF82FmGnnq2sUbTRsid9f2ahExrbcvCgjjOCP5v_Ei2XozZ_W5umzibu2KK5P_8JsVFYRDRwYp9wnltaHWgmPaZCROwgyQCMBD_JSqUp-2OxIfVf-47f02Y5HqNR-UHioT1XzAUE6_86W7K9UvNaTNtI7TDW_1yfBo8mF0pGNmYpfXGiJLrFiEP3v4"
              alt="Futuristic skyscraper architectural detail"
              fill
              sizes="(min-width: 768px) 33vw, 100vw"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent" />
            <div className="absolute bottom-8 left-8 right-8">
              <span className="mb-2 block text-[10px] font-bold uppercase tracking-[0.2em] text-primary">
                Our Culture
              </span>
              <h3 className="text-xl font-bold leading-tight text-white">
                We build structures <br />
                for human potential.
              </h3>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

