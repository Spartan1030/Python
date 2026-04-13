import type { Metadata } from "next";
import Image from "next/image";
import { Eye, Globe2, UsersRound } from "lucide-react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNav } from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "About Us",
  description: "Learn about Wenit Solutions: mission, vision, and global reach.",
};

export default function AboutPage() {
  return (
    <div className="flex flex-1 flex-col">
      <SiteNav activeHref="/about" />

      <main className="pt-24">
        <section className="relative flex min-h-[819px] items-center overflow-hidden px-6 md:px-12">
          <div className="absolute inset-0 z-0">
            <div className="absolute inset-0 z-10 bg-gradient-to-r from-background via-background/80 to-transparent" />
            <Image
              className="h-full w-full object-cover opacity-40 grayscale"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuAA7x8u9r2HD4Xt8xqfS_XkdaWNbf8eP1JE0ksVQuBnVzWQKpkbw3a5pZm2l2lhOvb-h0mnvdT3rFOWOnsKz2moBmtssr8HWGOUHAYYR7x2lixE-Yk8dep2HKWiTz8YGra4yrUR6g07nyuF_36AgNGv96wS1cKintJDEu0mGrmQzag-4TRRC30w3FDmKGOsuZCrQkoUlg0jGUG0AeY_g8YDwWPIDF-wb73BbN8qHh8dwqiAw84cuJ5nhJANTpUBdCquRfNIBDih07Y"
              alt="Monochrome glass skyscraper under a dramatic sky"
              fill
              priority
              sizes="100vw"
            />
          </div>

          <div className="relative z-20 mx-auto w-full max-w-screen-2xl">
            <div className="max-w-4xl">
              <span className="mb-6 block text-xs font-bold uppercase tracking-[0.3em] text-secondary">
                The Digital Consigliere
              </span>
              <h1 className="mb-8 text-6xl font-extrabold leading-none tracking-tighter text-primary md:text-8xl">
                ARCHITECTS OF <br /> HUMAN CAPITAL
              </h1>
              <p className="max-w-2xl text-xl font-light leading-relaxed text-on-surface-variant">
                We don&apos;t just fill seats. We engineer growth through a
                clandestine network of strategic talent, acting as the silent
                advisor to the world&apos;s most ambitious enterprises.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-surface-container-low px-6 py-32 md:px-12">
          <div className="mx-auto grid max-w-7xl grid-cols-1 gap-12 md:grid-cols-12 md:items-center">
            <div className="relative md:col-span-5">
              <div className="pointer-events-none absolute -top-12 -left-12 select-none text-[12rem] font-extrabold leading-none text-white/5">
                01
              </div>
              <h2 className="mb-8 text-4xl font-bold tracking-tight">
                OUR LEGACY
              </h2>
              <div className="mb-6 h-0.5 w-[30%] bg-secondary" />
              <p className="mb-6 text-lg leading-relaxed text-on-surface-variant">
                Founded on the principles of structural integrity and absolute
                discretion, Wenit Solutions emerged from the need for a more
                sophisticated approach to global staffing.
              </p>
              <p className="text-lg leading-relaxed text-on-surface-variant">
                What began as a boutique advisory has evolved into a global
                engine of talent architecture, bridging the gap between vision
                and execution.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 md:col-span-7">
              <div className="pt-12">
                <div className="relative h-[400px] overflow-hidden rounded-xl">
                  <Image
                    className="h-full w-full object-cover grayscale transition-all duration-700 hover:grayscale-0"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuBH1rCiYpfxUsHPYwJuwSks9puOG9OZW-29gzlx7nMsFpYMueLG5AccsHpmwslfvbFlklozo7PkAG6AGmP2eJvlUnB-_XAs16zppE875jnZFT588snYlwoIu1FAn04lAeaJUxspINGpXZO9Hord7r24vCWX2ns_MprF1g69E0RDu3Cg6DV6JRDKmNivlC3mZdf53X80_8M8CZgz5hTlMyYGpH4dnPeuNlrHIGoJO2v0FYxPpiux2_isqLwFjzQXl1m23Dikhg9t5dE"
                    alt="Professional adjusting a cufflink"
                    fill
                    sizes="(min-width: 768px) 35vw, 100vw"
                  />
                </div>
              </div>
              <div>
                <div className="relative h-[400px] overflow-hidden rounded-xl">
                  <Image
                    className="h-full w-full object-cover grayscale brightness-50"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuCQlmLyviBU8wtCbL0r0a-YrgA8aMyP70pVhsmFgz8ZLoGgoClufJKy1ryqe-Bnuixq846-marKm0uSfi0oFvOcB3vkSd_wnmiHG_L06i7mBPvB4wWvTGbGwNKFPxE5_FKGYSggz2YECHEgqEQqoszdTUlCdh3OmaLlOybMhzBQrGmU9pXDsuO-WuXyYEHW8l5NUHRwckJSZ7b625FTy1ko0mXJtUp7GgyO_0-4ywplo8AhWfQbfcTIliMOD4cHQmMcdu_bCVLZ2CQ"
                    alt="Minimalist office interior with glass walls"
                    fill
                    sizes="(min-width: 768px) 35vw, 100vw"
                  />
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-7xl px-6 py-32 md:px-12">
          <div className="grid grid-cols-1 gap-8 md:grid-cols-2">
            <div className="rounded-xl border border-white/5 bg-surface-variant/60 p-12 backdrop-blur-2xl transition-all hover:shadow-2xl hover:shadow-primary/5">
              <UsersRound className="mb-8 h-10 w-10 text-secondary" />
              <h3 className="mb-6 text-3xl font-bold tracking-tight">
                The Mission
              </h3>
              <p className="text-lg leading-relaxed text-on-surface-variant">
                To curate and deploy the world&apos;s most elite technical and
                creative minds into environments where they don&apos;t just
                function—they thrive. We build the scaffolding for corporate
                evolution.
              </p>
            </div>

            <div className="rounded-xl border border-white/5 bg-surface-variant/60 p-12 backdrop-blur-2xl transition-all hover:shadow-2xl hover:shadow-primary/5 md:mt-16">
              <Eye className="mb-8 h-10 w-10 text-secondary" />
              <h3 className="mb-6 text-3xl font-bold tracking-tight">
                The Vision
              </h3>
              <p className="text-lg leading-relaxed text-on-surface-variant">
                A future where the friction of recruitment is replaced by the
                precision of architecture. We aim to be the global standard for
                high-stakes talent placement and strategic consulting.
              </p>
            </div>
          </div>
        </section>

        <section className="bg-surface-container-lowest py-32">
          <div className="mx-auto max-w-7xl px-6 md:px-12">
            <div className="mb-16 text-center">
              <h2 className="mb-4 text-4xl font-bold tracking-tight">
                GLOBAL NODES
              </h2>
              <p className="text-on-surface-variant">
                Strategically positioned to influence every major market.
              </p>
            </div>

            <div className="relative h-[600px] w-full overflow-hidden rounded-2xl border border-white/5 bg-slate-900">
              <Image
                className="h-full w-full object-cover opacity-30 mix-blend-screen"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuBIS3hd7T32jIOgAi3XaNRPOzCPphhMlBRA_ROfEg3D-q0WNOSHAKeWUbc_0c5Tr9sjkYCDsujtwsEaJJYJDfNv_2uevy7U3f-EXVrlnVGu-fHBirVgImXialjlobd-9W2FaU257opBhccqFlNLOS-gEfbif2DvuY_NFPk3GN6c9C8lZY2TxzJSVISIPoMsJ6QsqPnN-qhkjjwl7Pt2ppbxIz592egx30W9WhJs39cioEmBUKp5X-KVtuT_wmO1Ltn7vY89PavfPKw"
                alt="Stylized dark world map with glowing nodes"
                fill
                sizes="100vw"
              />

              <div className="absolute top-[30%] left-[20%]">
                <div className="h-3 w-3 animate-pulse rounded-full bg-secondary shadow-[0_0_15px_#e9c176]" />
              </div>
              <div className="absolute top-[35%] left-[48%]">
                <div className="h-3 w-3 animate-pulse rounded-full bg-secondary shadow-[0_0_15px_#e9c176]" />
              </div>
              <div className="absolute top-[50%] left-[55%]">
                <div className="h-3 w-3 animate-pulse rounded-full bg-secondary shadow-[0_0_15px_#e9c176]" />
              </div>
              <div className="absolute top-[60%] left-[75%]">
                <div className="h-3 w-3 animate-pulse rounded-full bg-secondary shadow-[0_0_15px_#e9c176]" />
              </div>

              <div className="pointer-events-none absolute inset-0 border-[32px] border-background/20" />

              <div className="absolute left-6 bottom-6 inline-flex items-center gap-2 rounded-full border border-white/5 bg-surface-variant/60 px-4 py-2 backdrop-blur-2xl">
                <Globe2 className="h-4 w-4 text-secondary" />
                <span className="text-[10px] font-bold uppercase tracking-widest text-secondary">
                  Global Coverage
                </span>
              </div>
            </div>
          </div>
        </section>
      </main>

      <SiteFooter />
    </div>
  );
}

