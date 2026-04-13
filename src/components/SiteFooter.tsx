import Link from "next/link";
import { Globe, Share2 } from "lucide-react";

export function SiteFooter() {
  return (
    <footer className="w-full border-t border-white/5 bg-slate-950 pt-24 pb-12">
      <div className="mx-auto mb-20 grid max-w-7xl grid-cols-1 gap-12 px-6 md:grid-cols-4 md:px-12">
        <div className="md:col-span-1">
          <div className="mb-6 text-lg font-semibold uppercase tracking-tighter text-slate-200">
            Wenit Solutions
          </div>
          <p className="text-xs leading-relaxed text-slate-500">
            Structural engineering for the world&apos;s most ambitious human
            capital projects. Strategic talent architecture across permanent,
            contract, and payroll domains.
          </p>
        </div>

        <div>
          <h5 className="mb-6 text-xs font-bold uppercase tracking-widest text-slate-400">
            Company
          </h5>
          <ul className="space-y-4">
            <li>
              <Link
                className="text-xs uppercase tracking-widest text-slate-500 transition-colors hover:text-amber-100"
                href="/about"
              >
                About Us
              </Link>
            </li>
            <li>
              <a
                className="text-xs uppercase tracking-widest text-slate-500 transition-colors hover:text-amber-100"
                href="#"
              >
                Privacy Policy
              </a>
            </li>
            <li>
              <a
                className="text-xs uppercase tracking-widest text-slate-500 transition-colors hover:text-amber-100"
                href="#"
              >
                Terms
              </a>
            </li>
          </ul>
        </div>

        <div>
          <h5 className="mb-6 text-xs font-bold uppercase tracking-widest text-slate-400">
            Services
          </h5>
          <ul className="space-y-4">
            <li>
              <Link
                className="text-xs uppercase tracking-widest text-slate-500 transition-colors hover:text-amber-100"
                href="/services"
              >
                Our Services
              </Link>
            </li>
            <li>
              <Link
                className="text-xs uppercase tracking-widest text-slate-500 transition-colors hover:text-amber-100"
                href="/jobs"
              >
                Job Openings
              </Link>
            </li>
            <li>
              <Link
                className="text-xs uppercase tracking-widest text-slate-500 transition-colors hover:text-amber-100"
                href="/contact"
              >
                Contact Us
              </Link>
            </li>
          </ul>
        </div>

        <div>
          <h5 className="mb-6 text-xs font-bold uppercase tracking-widest text-slate-400">
            Connect
          </h5>
          <div className="flex gap-6">
            <a
              className="text-amber-200 transition-all hover:text-amber-100"
              href="#"
              aria-label="Website"
            >
              <Globe className="h-5 w-5" />
            </a>
            <a
              className="text-amber-200 transition-all hover:text-amber-100"
              href="#"
              aria-label="Share"
            >
              <Share2 className="h-5 w-5" />
            </a>
          </div>
        </div>
      </div>

      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 border-t border-white/5 px-6 pt-12 md:flex-row md:px-12">
        <p className="text-xs uppercase tracking-widest text-slate-400 opacity-80">
          © 2024 Wenit Solutions. GSTIN: 27AAACW1234F1Z5. Strategic Talent
          Architecture.
        </p>
      </div>
    </footer>
  );
}

