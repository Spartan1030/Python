import type { Metadata } from "next";
import Image from "next/image";
import {
  Bolt,
  Lock,
  Mail,
  Phone,
  UploadCloud,
  UserRoundPen,
  Verified,
} from "lucide-react";
import { SiteFooter } from "@/components/SiteFooter";
import { SiteNav } from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Upload Resume",
  description: "Upload your resume to be matched with high-stakes opportunities.",
};

export default function UploadResumePage() {
  return (
    <div className="flex flex-1 flex-col">
      <SiteNav activeHref="/upload-resume" />

      <main className="mx-auto flex min-h-screen w-full max-w-7xl flex-col items-center px-6 pt-32 pb-24 md:px-12">
        <header className="mb-16 max-w-3xl text-center">
          <span className="mb-4 block text-xs uppercase tracking-[0.2em] text-secondary">
            Strategic Talent Architecture
          </span>
          <h1 className="mb-6 text-5xl font-extrabold leading-tight tracking-tight text-white md:text-7xl">
            Accelerate Your <br /> Career Pivot.
          </h1>
          <p className="text-lg font-light text-on-surface-variant md:text-xl">
            Our AI-driven parsing engine extracts your expertise instantly. No
            more redundant manual entry—just precise alignment with high-stakes
            opportunities.
          </p>
        </header>

        <div className="grid w-full grid-cols-1 items-start gap-12 lg:grid-cols-12">
          <div className="space-y-8 lg:col-span-7">
            <div className="group flex min-h-[400px] flex-col items-center justify-center rounded-xl border-2 border-dashed border-outline-variant/30 bg-surface-variant/60 p-12 backdrop-blur-2xl transition-all duration-500 hover:border-secondary/40">
              <div className="mb-8 flex h-20 w-20 items-center justify-center rounded-full bg-surface-container-highest shadow-xl">
                <UploadCloud className="h-10 w-10 text-secondary" />
              </div>
              <h3 className="mb-2 text-2xl font-bold text-white">
                Drop your resume here
              </h3>
              <p className="mb-8 font-light text-on-surface-variant">
                PDF, DOCX, or RTF (Max 10MB)
              </p>
              <button
                className="rounded-md bg-[linear-gradient(135deg,#b9c7e4_0%,#0a192f_100%)] px-10 py-4 font-semibold text-on-primary shadow-2xl transition-all duration-300 hover:shadow-primary/20 active:scale-95"
                type="button"
              >
                Choose File
              </button>
              <div className="mt-12 flex items-center gap-4 rounded-full border border-white/5 bg-surface-container-lowest/50 px-4 py-2 text-xs uppercase tracking-widest text-on-surface-variant">
                <Bolt className="h-4 w-4 text-secondary" />
                AI-DRIVEN RESUME PARSING ENABLED
              </div>
            </div>

            <div className="space-y-6 rounded-xl bg-surface-container-low p-8">
              <div className="mb-2 flex items-end justify-between">
                <div className="space-y-1">
                  <p className="text-sm uppercase tracking-wider text-secondary">
                    Parsing Status
                  </p>
                  <h4 className="font-medium text-white">
                    Extracting professional history...
                  </h4>
                </div>
                <span className="text-xl font-bold text-secondary">68%</span>
              </div>
              <div className="h-1 w-full overflow-hidden rounded-full bg-surface-container-highest">
                <div className="h-full w-2/3 bg-secondary transition-all duration-1000 ease-out" />
              </div>
              <div className="flex gap-6">
                <div className="flex items-center gap-2">
                  <Verified className="h-4 w-4 text-secondary" />
                  <span className="text-xs text-on-surface-variant">
                    File Integrity Verified
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Verified className="h-4 w-4 text-secondary" />
                  <span className="text-xs text-on-surface-variant">
                    Skills Mapping Initiated
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-8 lg:col-span-5">
            <div className="space-y-8 rounded-xl bg-surface-container p-10">
              <h3 className="flex items-center gap-3 text-xl font-bold text-white">
                <UserRoundPen className="h-5 w-5 text-secondary" />
                Verify Contact Details
              </h3>

              <div className="space-y-6">
                <div className="relative">
                  <label className="mb-2 block text-[10px] uppercase tracking-widest text-on-surface-variant">
                    Primary Email
                  </label>
                  <input
                    className="w-full rounded-t-lg bg-surface-container-lowest px-4 py-3 text-on-surface outline-none transition-all focus:border-secondary border-b-2 border-transparent"
                    placeholder="alex.architect@talent.com"
                    type="email"
                  />
                </div>
                <div className="relative">
                  <label className="mb-2 block text-[10px] uppercase tracking-widest text-on-surface-variant">
                    Phone Number
                  </label>
                  <input
                    className="w-full rounded-t-lg bg-surface-container-lowest px-4 py-3 text-on-surface outline-none transition-all focus:border-secondary border-b-2 border-transparent"
                    placeholder="+1 (555) 000-0000"
                    type="tel"
                  />
                </div>
                <div className="relative">
                  <label className="mb-2 block text-[10px] uppercase tracking-widest text-on-surface-variant">
                    LinkedIn URL
                  </label>
                  <input
                    className="w-full rounded-t-lg bg-surface-container-lowest px-4 py-3 text-on-surface outline-none transition-all focus:border-secondary border-b-2 border-transparent"
                    placeholder="linkedin.com/in/alex-architect"
                    type="url"
                  />
                </div>
              </div>

              <button
                className="w-full rounded-md border border-white/5 bg-surface-bright py-4 font-semibold text-on-surface transition-all duration-200 hover:bg-surface-container-highest active:scale-[0.98]"
                type="button"
              >
                Confirm &amp; Process
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="rounded-xl border border-white/5 bg-surface-container-low p-6">
                <Mail className="mb-3 h-5 w-5 text-secondary" />
                <h4 className="text-xs font-bold uppercase tracking-tighter text-white">
                  GDPR Compliant
                </h4>
                <p className="mt-1 text-[10px] leading-relaxed text-on-surface-variant">
                  Your data is encrypted and stored in EEA-compliant servers.
                </p>
              </div>
              <div className="rounded-xl border border-white/5 bg-surface-container-low p-6">
                <Lock className="mb-3 h-5 w-5 text-secondary" />
                <h4 className="text-xs font-bold uppercase tracking-tighter text-white">
                  256-bit Encryption
                </h4>
                <p className="mt-1 text-[10px] leading-relaxed text-on-surface-variant">
                  Secure end-to-end transmission for all candidate dossiers.
                </p>
              </div>
            </div>

            <div className="group relative aspect-video overflow-hidden rounded-xl">
              <Image
                className="h-full w-full object-cover opacity-40 grayscale transition-transform duration-700 group-hover:scale-105"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuDkxcnaYKBv2rM9jFcxP_IRuBZKhOoAVM6YOfYjD9_GEWafCyvKHHkaJblnrRe6gB82djGb9fDp9MLKLds9Lq1iEeuKVL1CvATHYk2lGgKebs5ew7Y3sc-7c0WES7_sJvW59IhjvwoxL1QRF8ap1Chx4hG0Azyym-CEbeYkZ3vW4ZASuvywQT3yJ3HA4n_3-VJHveWnqWlf6OSmRqNdX8YM-_3ops4kJx2MNw5Lsi2kSWqqpUHq9qIvoQRJL57ZQR3yZHHR4805FUw"
                alt="High-end architectural workspace in deep blue lighting"
                fill
                sizes="(min-width: 768px) 40vw, 100vw"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent" />
              <div className="absolute bottom-4 left-4 right-4">
                <p className="text-[10px] uppercase tracking-widest text-secondary">
                  Precision Hiring Engine
                </p>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 rounded-xl border border-white/5 bg-surface-container-low p-6">
              <div className="flex items-center gap-3">
                <Mail className="h-4 w-4 text-secondary" />
                <span className="text-xs text-on-surface-variant">Email</span>
              </div>
              <div className="flex items-center gap-3">
                <Phone className="h-4 w-4 text-secondary" />
                <span className="text-xs text-on-surface-variant">Phone</span>
              </div>
              <div className="flex items-center gap-3">
                <Verified className="h-4 w-4 text-secondary" />
                <span className="text-xs text-on-surface-variant">Secure</span>
              </div>
            </div>
          </div>
        </div>
      </main>

      <SiteFooter />
    </div>
  );
}

