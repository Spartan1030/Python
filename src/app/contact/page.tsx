import type { Metadata } from "next";
import Image from "next/image";
import {
  AtSign,
  Building2,
  MapPin,
  Phone,
  Send,
  UserPlus,
} from "lucide-react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNav } from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Contact Us",
  description: "Start a consultation with Wenit Solutions.",
};

export default function ContactPage() {
  return (
    <div className="flex flex-1 flex-col">
      <SiteNav activeHref="/contact" />

      <main className="mx-auto w-full max-w-screen-2xl px-6 pt-32 pb-24 md:px-12">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12">
          <div className="space-y-12 lg:col-span-8">
            <header className="space-y-4">
              <span className="text-xs font-bold uppercase tracking-[0.2em] text-secondary">
                Consultation
              </span>
              <h1 className="text-5xl font-extrabold leading-tight tracking-tighter text-primary md:text-6xl">
                Strategic Talent <br />
                <span className="text-on-surface">Architecture.</span>
              </h1>
              <p className="max-w-xl text-lg font-light leading-relaxed text-on-surface-variant">
                Design your workforce with the precision of structural
                engineering. Tell us about your project requirements and we
                will architect the ideal team.
              </p>
            </header>

            <form className="space-y-16">
              <section className="space-y-8">
                <div className="flex items-center gap-4">
                  <span className="flex h-10 w-10 items-center justify-center rounded-full border border-outline-variant text-secondary font-bold">
                    01
                  </span>
                  <h2 className="text-xl font-semibold tracking-tight">
                    Company Foundation
                  </h2>
                </div>
                <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                  <div className="group space-y-2">
                    <label className="text-xs uppercase tracking-widest text-on-surface-variant transition-colors group-focus-within:text-secondary">
                      Company Name
                    </label>
                    <input
                      className="w-full bg-surface-container-lowest px-0 py-4 placeholder:text-outline/40 transition-all focus:outline-none border-b-2 border-outline-variant focus:border-secondary"
                      placeholder="e.g. Nexus Corp"
                      type="text"
                    />
                  </div>
                  <div className="group space-y-2">
                    <label className="text-xs uppercase tracking-widest text-on-surface-variant transition-colors group-focus-within:text-secondary">
                      Industry Vertical
                    </label>
                    <select className="w-full bg-surface-container-lowest px-0 py-4 text-on-surface-variant transition-all focus:outline-none border-b-2 border-outline-variant focus:border-secondary">
                      <option>Technological Infrastructure</option>
                      <option>Financial Systems</option>
                      <option>Biotech &amp; Health</option>
                      <option>Creative Design</option>
                    </select>
                  </div>
                </div>
              </section>

              <section className="space-y-8">
                <div className="flex items-center gap-4">
                  <span className="flex h-10 w-10 items-center justify-center rounded-full border border-outline-variant text-secondary font-bold">
                    02
                  </span>
                  <h2 className="text-xl font-semibold tracking-tight">
                    Talent Specification
                  </h2>
                </div>
                <div className="space-y-6">
                  <div className="group space-y-2">
                    <label className="text-xs uppercase tracking-widest text-on-surface-variant transition-colors group-focus-within:text-secondary">
                      Key Role Requirement
                    </label>
                    <input
                      className="w-full bg-surface-container-lowest px-0 py-4 placeholder:text-outline/40 transition-all focus:outline-none border-b-2 border-outline-variant focus:border-secondary"
                      placeholder="e.g. Senior Backend Architect"
                      type="text"
                    />
                  </div>
                  <div className="group space-y-2">
                    <label className="text-xs uppercase tracking-widest text-on-surface-variant transition-colors group-focus-within:text-secondary">
                      Role Description &amp; Critical Skills
                    </label>
                    <textarea
                      className="w-full resize-none bg-surface-container-lowest px-0 py-4 placeholder:text-outline/40 transition-all focus:outline-none border-b-2 border-outline-variant focus:border-secondary"
                      placeholder="Detail the core competencies and architectural challenges..."
                      rows={4}
                    />
                  </div>
                </div>
              </section>

              <section className="space-y-8">
                <div className="flex items-center gap-4">
                  <span className="flex h-10 w-10 items-center justify-center rounded-full border border-outline-variant text-secondary font-bold">
                    03
                  </span>
                  <h2 className="text-xl font-semibold tracking-tight">
                    Engagement Model
                  </h2>
                </div>
                <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
                  {[
                    {
                      title: "Permanent",
                      desc: "Long-term strategic growth hires.",
                      Icon: UserPlus,
                    },
                    {
                      title: "Contract",
                      desc: "Agile specialized project scaling.",
                      Icon: Building2,
                    },
                    {
                      title: "Payroll",
                      desc: "Comprehensive backend management.",
                      Icon: Send,
                    },
                  ].map(({ title, desc, Icon }) => (
                    <label key={title} className="group cursor-pointer">
                      <input className="peer hidden" name="engagement" type="radio" />
                      <div className="relative overflow-hidden rounded-lg border border-outline-variant/10 bg-surface-container-low p-6 transition-all group-hover:bg-surface-container peer-checked:border-secondary peer-checked:bg-surface-container-high">
                        <div className="absolute top-0 left-0 h-1 w-full bg-secondary opacity-0 transition-opacity peer-checked:opacity-100" />
                        <Icon className="mb-3 h-5 w-5 text-secondary" />
                        <h3 className="text-sm font-bold">{title}</h3>
                        <p className="mt-2 text-xs text-on-surface-variant">
                          {desc}
                        </p>
                      </div>
                    </label>
                  ))}
                </div>
              </section>

              <div className="pt-8">
                <button
                  className="w-full rounded-md bg-primary px-12 py-4 font-bold tracking-tight text-on-primary transition-all hover:-translate-y-1 hover:shadow-[0_0_20px_rgba(185,199,228,0.3)] md:w-auto"
                  type="button"
                >
                  Initialize Consultation
                </button>
              </div>
            </form>
          </div>

          <div className="space-y-8 lg:col-span-4">
            <div className="rounded-xl border border-white/5 bg-surface-variant/60 p-8 backdrop-blur-2xl shadow-2xl">
              <div className="relative">
                <div className="absolute top-0 left-0 h-0.5 w-[30%] bg-secondary" />
              </div>
              <h3 className="mb-8 text-2xl font-bold tracking-tight text-primary">
                Direct Nexus
              </h3>

              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-container-highest">
                    <AtSign className="h-5 w-5 text-secondary" />
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-widest text-on-surface-variant">
                      Email
                    </p>
                    <p className="text-lg font-medium">solutions@wenit.in</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-container-highest">
                    <Phone className="h-5 w-5 text-secondary" />
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-widest text-on-surface-variant">
                      Phone
                    </p>
                    <p className="text-lg font-medium">+91 (80) 4567 8900</p>
                  </div>
                </div>

                <div className="flex items-start gap-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-surface-container-highest">
                    <MapPin className="h-5 w-5 text-secondary" />
                  </div>
                  <div>
                    <p className="text-xs uppercase tracking-widest text-on-surface-variant">
                      Bengaluru Hub
                    </p>
                    <p className="text-sm font-light leading-relaxed text-on-surface-variant">
                      Suite 405, Prestige Sky,
                      <br />
                      Whitefield, Bengaluru - 560066
                    </p>
                  </div>
                </div>
              </div>

              <div className="mt-8 grid grid-cols-2 gap-4 border-t border-white/10 pt-8">
                <div className="flex flex-col items-center justify-center rounded bg-surface-container-lowest p-3 text-center">
                  <span className="mb-1 text-[10px] uppercase tracking-tighter text-outline">
                    GSTIN
                  </span>
                  <span className="text-[10px] font-bold text-on-surface">
                    27AAACW1234F
                  </span>
                </div>
                <div className="flex flex-col items-center justify-center rounded bg-surface-container-lowest p-3 text-center">
                  <span className="mb-1 text-[10px] uppercase tracking-tighter text-outline">
                    ISO Certified
                  </span>
                  <span className="text-[10px] font-bold text-on-surface">
                    9001:2015
                  </span>
                </div>
              </div>
            </div>

            <div className="group relative h-80 overflow-hidden rounded-xl border border-white/5">
              <Image
                className="h-full w-full object-cover grayscale brightness-50 contrast-125 transition-transform duration-700 group-hover:scale-105"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCSpLubokagjS5_B9GZ3t743YhttcKqEwhg7cNDnl3aFkEtwDXCXluARLDGJUbxx9tNO2yhmnC9WCOQhNTiNiYrH0lOi89hzJsFC9ro4_si3pweNMMX7zydWu5wUZ5xxmqDJepvbaE7ucziuWCtqByXJKuGWe0EodhTfCaSW91Zjczmxq9zMWvKeOPMhrQE9cZKistfwOrcEpCXpdsgfT9HhTVwXSLDlLJhjATPaeGaayBdTxwTYx0Kkls7TYnHLZj5elfbnGSZ3vw"
                alt="Stylized 3D architectural city map of Bengaluru"
                fill
                sizes="(min-width: 1024px) 33vw, 100vw"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
              <div className="absolute bottom-6 left-6">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 animate-pulse rounded-full bg-secondary" />
                  <span className="text-xs font-bold uppercase tracking-widest text-secondary">
                    Primary HQ
                  </span>
                </div>
                <p className="text-xl font-bold tracking-tight">
                  Bengaluru Hub
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <SiteFooter />
    </div>
  );
}

