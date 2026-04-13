import type { Metadata } from "next";
import Image from "next/image";
import { CheckCircle2, CreditCard, Layers3, ShieldCheck } from "lucide-react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNav } from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Services",
  description: "Permanent recruitment, contract staffing, payroll, and compliance services.",
};

export default function ServicesPage() {
  return (
    <div className="flex flex-1 flex-col">
      <SiteNav activeHref="/services" />

      <main className="pt-24">
        <section className="relative mx-auto flex h-[716px] max-w-7xl items-center overflow-hidden px-6 md:px-12">
          <div className="z-10 w-full md:w-2/3">
            <span className="mb-4 block text-xs uppercase tracking-[0.2em] text-secondary">
              Structural Precision
            </span>
            <h1 className="text-6xl font-extrabold leading-[0.9] tracking-tighter text-primary md:text-8xl">
              Strategic Talent <br />{" "}
              <span className="text-on-surface-variant/50">
                Architecture
              </span>
            </h1>
            <p className="mt-8 max-w-md text-lg leading-relaxed text-on-surface-variant">
              We don&apos;t just recruit; we engineer human capital ecosystems
              through curated selection and technical mastery.
            </p>
          </div>

          <div className="pointer-events-none absolute right-0 top-1/2 h-full w-1/2 -translate-y-1/2 opacity-20">
            <Image
              className="h-full w-full object-cover mix-blend-overlay"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuBEn67mes2r0tPolpcydIiYdIrx0I693z5X8f1TRQfx1Aj5Mm3psekXEQPkpLLpExBRZ_utj6Oe8Ca2xDq0MTdmDXAtX5Rxu9zMt3OKu8nS4WMGS4P2Vc5i5VZYjYNk0-1pWMmqCOavFCLjtrf6JDYOjkekN7_ZGZHUYfjzaWFLBHcM3QWaHJDhG6_NwQkI2NvnkkI6FNX-2LoaqZt4CgfEpv_AThmOhGDO5wr7WQtXbGl--EI_jjmHK0rq2vEUAJCcilZhErx4Bz0"
              alt="Abstract architectural blueprint lines"
              fill
              sizes="(min-width: 768px) 50vw, 100vw"
            />
          </div>
        </section>

        <section className="bg-surface-container-low px-6 py-24 md:px-12">
          <div className="mx-auto grid max-w-7xl grid-cols-1 gap-8 md:grid-cols-3">
            <div className="relative rounded-xl border-t border-primary/10 bg-surface-variant/60 p-10 backdrop-blur-2xl transition-all duration-500 hover:bg-surface-container-high">
              <div className="mb-8">
                <CreditCard className="h-10 w-10 text-secondary" />
              </div>
              <h3 className="mb-4 text-2xl font-bold tracking-tight text-primary">
                Permanent Recruitment
              </h3>
              <p className="mb-8 text-sm leading-relaxed text-on-surface-variant">
                Building the foundation of your enterprise with long-term
                vision. We identify cultural fits and technical masters who
                define your future.
              </p>
              <span className="text-xs font-bold uppercase tracking-widest text-secondary">
                Explore Blueprint
              </span>
            </div>

            <div className="relative rounded-xl border-t border-primary/10 bg-surface-variant/60 p-10 backdrop-blur-2xl transition-all duration-500 hover:bg-surface-container-high">
              <div className="mb-8">
                <Layers3 className="h-10 w-10 text-secondary" />
              </div>
              <h3 className="mb-4 text-2xl font-bold tracking-tight text-primary">
                Contract Staffing
              </h3>
              <p className="mb-8 text-sm leading-relaxed text-on-surface-variant">
                Agile structural support for dynamic project cycles. Scale your
                workforce with precision-vetted technical consultants.
              </p>
              <span className="text-xs font-bold uppercase tracking-widest text-secondary">
                Adaptive Logic
              </span>
            </div>

            <div className="relative rounded-xl border-t border-primary/10 bg-surface-variant/60 p-10 backdrop-blur-2xl transition-all duration-500 hover:bg-surface-container-high">
              <div className="mb-8">
                <ShieldCheck className="h-10 w-10 text-secondary" />
              </div>
              <h3 className="mb-4 text-2xl font-bold tracking-tight text-primary">
                Seamless Payroll
              </h3>
              <p className="mb-8 text-sm leading-relaxed text-on-surface-variant">
                Automated compliance and financial flow. Zero-friction
                processing that allows your core team to focus on innovation.
              </p>
              <span className="text-xs font-bold uppercase tracking-widest text-secondary">
                Fluid Systems
              </span>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-32 md:px-12">
          <div className="mb-16">
            <h2 className="mb-4 text-4xl font-extrabold tracking-tighter text-primary">
              Strategic Matrix
            </h2>
            <div className="h-1 w-24 bg-secondary" />
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-left">
              <thead>
                <tr className="border-b border-outline-variant/30 text-xs font-medium uppercase tracking-widest text-secondary">
                  <th className="px-4 py-6">Feature Set</th>
                  <th className="px-4 py-6">Permanent</th>
                  <th className="px-4 py-6">Contract</th>
                  <th className="px-4 py-6">Payroll</th>
                </tr>
              </thead>
              <tbody className="text-on-surface">
                <tr className="border-b border-outline-variant/10 transition-colors hover:bg-white/5">
                  <td className="px-4 py-8 font-semibold text-primary">
                    Time-to-Value
                  </td>
                  <td className="px-4 py-8">Long-term (30+ days)</td>
                  <td className="px-4 py-8">Immediate (2-5 days)</td>
                  <td className="px-4 py-8">Ongoing</td>
                </tr>
                <tr className="border-b border-outline-variant/10 transition-colors hover:bg-white/5">
                  <td className="px-4 py-8 font-semibold text-primary">
                    Risk Mitigation
                  </td>
                  <td className="px-4 py-8">Replacement Guarantee</td>
                  <td className="px-4 py-8">Project Milestones</td>
                  <td className="px-4 py-8">Compliance Liability</td>
                </tr>
                <tr className="border-b border-outline-variant/10 transition-colors hover:bg-white/5">
                  <td className="px-4 py-8 font-semibold text-primary">
                    Scalability
                  </td>
                  <td className="px-4 py-8">Incremental</td>
                  <td className="px-4 py-8">Elastic</td>
                  <td className="px-4 py-8">Enterprise-wide</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <section className="bg-surface-container px-6 py-32 md:px-12">
          <div className="mx-auto flex max-w-7xl flex-col items-center gap-20 md:flex-row">
            <div className="relative w-full md:w-1/2">
              <div className="relative aspect-square overflow-hidden rounded-lg bg-surface-container-highest shadow-2xl">
                <Image
                  className="h-full w-full object-cover"
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuCg_Jsr1MtlB9oCmg_XgHRGyV8PP1pI-lVoJng8IqUodij-x7gsuOCccKnHk6Fg-TrvcULp2pga6gZM_KkS7g5MVrpApbhKuCL2L72cujISKN1bcamdq8KCLg1Ho9oH6eNU1SU4UHBhs8vBrL3erqH4PuKK9mvKz39vAIPCwWVo0cyoeQoq0UYTV64stibwkF85uHcHlBOVDbLQ9y9WgOAV9UibkIGZdlbOqGz6HYJV_n3zTqXMAvZXKwCGJ1Lw_aWSI7N80w9N5-4"
                  alt="Precision robotic arm in a futuristic lab"
                  fill
                  sizes="(min-width: 768px) 50vw, 100vw"
                />
                <div className="absolute inset-0 mix-blend-color bg-primary/10" />
              </div>

              <div className="absolute -bottom-6 -right-6 max-w-xs border-t border-primary/10 bg-surface-variant/60 p-8 backdrop-blur-2xl shadow-2xl">
                <span className="mb-2 block text-4xl font-bold text-secondary">
                  98%
                </span>
                <span className="text-xs font-semibold uppercase tracking-widest text-on-surface-variant">
                  Placement Success Rate through Academy Training
                </span>
              </div>
            </div>

            <div className="w-full md:w-1/2">
              <span className="mb-4 block text-xs uppercase tracking-[0.2em] text-secondary">
                The Wenit Academy
              </span>
              <h2 className="mb-8 text-5xl font-extrabold leading-tight tracking-tighter text-primary">
                Manufacturing Talent <br />
                for the Digital Age
              </h2>
              <p className="mb-8 leading-relaxed text-on-surface-variant">
                We don&apos;t wait for the right talent to emerge. We manufacture
                it. Our Academy identifies high-potential individuals and
                sculpts them through rigorous architectural training in emerging
                technologies, ensuring they arrive on day one ready to build.
              </p>
              <ul className="space-y-4">
                {[
                  "Customized Skill Architecting",
                  "Real-world Project Simulation",
                  "Continuous Evolution Framework",
                ].map((text) => (
                  <li key={text} className="flex items-center gap-4 text-sm text-primary">
                    <CheckCircle2 className="h-5 w-5 text-secondary" />
                    {text}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

