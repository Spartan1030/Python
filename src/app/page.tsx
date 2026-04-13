import Image from "next/image";
import Link from "next/link";
import { ArrowRight, BadgeCheck, Building2, Landmark, Search } from "lucide-react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNav } from "@/components/SiteNav";

export default function Home() {
  return (
    <div className="flex flex-1 flex-col">
      <SiteNav activeHref="/" />

      <main className="pt-20">
        <section className="relative flex min-h-[921px] items-center overflow-hidden px-6 md:px-12">
          <div className="absolute inset-0 z-0">
            <Image
              className="h-full w-full object-cover opacity-40 mix-blend-luminosity"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuBrQHiSloTDZ0vbpJdlGRNN9TYg-luulETV6l8j8qerdpwG44bMM1oRNLciUCjmBLBl9az1r69ZLHaRK_GcNZlFiTMc0J20BOkXTWQxNkj7gICDQlFBT1H4n6K_aY1O8Kk4TI4JaeCe20DXhDIcJRXFHt98ayKrFkPY5tyrpGzgBTEoCdcLtNUjDRGXnS1q-VyC7u6gRfnGg-m-xmqBbSCdmLSU0xLZJtcDUpGZeDZuwOGJqZ25_O9Om9G0TK1xyWc6v8etf1vRUd4"
              alt="Monochrome architectural shot of a glass skyscraper at twilight"
              fill
              priority
              sizes="100vw"
            />
            <div className="absolute inset-0 bg-gradient-to-r from-background via-background/80 to-transparent" />
          </div>

          <div className="relative z-10 mx-auto w-full max-w-screen-2xl">
            <div className="max-w-4xl">
              <div className="mb-8 inline-flex items-center gap-2 rounded-full border border-white/5 bg-surface-container-highest/40 px-3 py-1 backdrop-blur-md">
                <span className="h-2 w-2 animate-pulse rounded-full bg-secondary" />
                <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-secondary">
                  2025 Readiness Certified
                </span>
              </div>

              <h1 className="mb-8 text-6xl font-extrabold leading-[0.9] tracking-tighter text-on-surface md:text-8xl">
                Architects of <br />
                <span className="italic text-primary">Human Potential</span>
              </h1>

              <p className="mb-12 max-w-xl text-xl font-light leading-relaxed text-on-surface-variant">
                Engineering strategic talent ecosystems through precise
                recruitment, seamless payroll, and future-forward staffing
                architecture.
              </p>

              <div className="flex flex-wrap gap-6">
                <Link
                  href="/contact"
                  className="rounded-md bg-primary px-8 py-4 text-sm font-bold uppercase tracking-widest text-on-primary transition-all hover:shadow-[0_0_20px_rgba(185,199,228,0.2)]"
                >
                  Hire Talent
                </Link>
                <Link
                  href="/jobs"
                  className="rounded-md border border-outline-variant px-8 py-4 text-sm font-bold uppercase tracking-widest text-on-surface transition-all hover:bg-white/5"
                >
                  Find a Job
                </Link>
              </div>
            </div>

            <div className="absolute bottom-12 right-12 hidden lg:block">
              <div className="max-w-xs rounded-xl border border-white/5 bg-surface-variant/60 p-6 backdrop-blur-2xl shadow-[0_0_40px_rgba(185,199,228,0.05)]">
                <div className="mb-4 flex items-start justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-widest text-secondary">
                    Live Reputation
                  </span>
                  <BadgeCheck className="h-4 w-4 text-secondary" />
                </div>
                <div className="space-y-4">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded bg-surface-container-highest">
                      <Building2 className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-xs font-bold text-on-surface">
                        Global Tech Hub
                      </p>
                      <p className="text-[10px] text-on-surface-variant">
                        Permanent Staffing • 2m ago
                      </p>
                    </div>
                  </div>
                  <div className="h-px bg-outline-variant/20" />
                  <div className="flex items-center gap-4 opacity-50">
                    <div className="flex h-10 w-10 items-center justify-center rounded bg-surface-container-highest">
                      <Landmark className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <p className="text-xs font-bold text-on-surface">
                        Fin-Solutions Inc
                      </p>
                      <p className="text-[10px] text-on-surface-variant">
                        Contractual • 15m ago
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-screen-2xl px-6 py-32 md:px-12">
          <div className="mb-20 flex flex-col justify-between gap-8 md:flex-row md:items-end">
            <div className="max-w-2xl">
              <span className="mb-4 block text-[10px] font-bold uppercase tracking-[0.3em] text-secondary">
                Service Infrastructure
              </span>
              <h2 className="text-5xl font-bold tracking-tighter">
                The Strategic Blueprint
              </h2>
            </div>
            <p className="max-w-sm text-sm leading-relaxed text-on-surface-variant">
              A multi-layered approach to talent acquisition, ensuring structural
              integrity in your workforce composition.
            </p>
          </div>

          <div className="grid min-h-[700px] grid-cols-1 gap-6 md:grid-cols-6 md:grid-rows-2">
            <div className="group relative overflow-hidden rounded-2xl border border-white/5 bg-surface-variant/60 md:col-span-3 md:row-span-2">
              <div className="absolute inset-0">
                <Image
                  className="h-full w-full object-cover opacity-30 transition-transform duration-700 group-hover:scale-110"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuBbpRKUbhpLpdgwbCBrZaqwGvjRsRA6uLIlCajVy3ITA2tPQvtlR10UTzVobcRYeb6MhcEZCPt9I9H1qzcQYvBuyjKBaHLbha6RzVWZfOoEJoGuuO-U5TSmxpZNsVJYocz8ph6F7tppAA52DlTS-04NpWQMzH3OK5DcBvpuoaGpxjowhYJm7OGzvoIQ3hLspAYBShoc91lI5ad2vWiMUiNP1X3kCGRb7e8wY0mkQy52mGYIivDv67x96Bhd_ggo-Qh1tanXRa2tVIs"
                  alt="Modern office interior with expansive windows"
                  fill
                  sizes="(min-width: 768px) 50vw, 100vw"
                />
              </div>
              <div className="relative z-10 flex h-full flex-col justify-end p-10">
                <div className="mb-8 h-1 w-12 bg-secondary transition-all duration-500 group-hover:w-24" />
                <h3 className="mb-4 text-3xl font-bold tracking-tight">
                  Permanent Recruitment
                </h3>
                <p className="mb-8 max-w-sm text-on-surface-variant">
                  Curating lifelong leadership and specialized expertise to form
                  your company&apos;s core foundation.
                </p>
                <Link
                  href="/services"
                  className="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-primary transition-all group-hover:gap-4"
                >
                  Explore Architecture <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            </div>

            <div className="group flex flex-col justify-between rounded-2xl border border-white/5 bg-surface-container-low p-10 md:col-span-3 md:row-span-1">
              <div className="flex items-start justify-between">
                <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-surface-container-highest">
                  <Search className="h-7 w-7 text-secondary" />
                </div>
                <span className="font-mono text-xs text-outline">SRV-02</span>
              </div>
              <div>
                <h3 className="mb-2 text-2xl font-bold tracking-tight">
                  Contractual Staffing
                </h3>
                <p className="text-sm text-on-surface-variant opacity-0 transition-opacity group-hover:opacity-100">
                  Agile talent deployment for high-impact projects.
                </p>
              </div>
            </div>

            <div className="flex cursor-pointer flex-col justify-between rounded-2xl border border-white/5 bg-surface-container p-10 transition-colors hover:bg-surface-container-high md:col-span-2 md:row-span-1">
              <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                <Landmark className="h-6 w-6 text-primary" />
              </div>
              <h3 className="text-xl font-bold tracking-tight">
                Seamless Payroll
              </h3>
            </div>

            <div className="flex flex-col items-center justify-center rounded-2xl bg-[linear-gradient(135deg,#b9c7e4_0%,#0a192f_100%)] p-8 text-center md:col-span-1 md:row-span-1">
              <span className="text-[10px] font-bold uppercase tracking-widest text-on-primary">
                Advisory
              </span>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}
