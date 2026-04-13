import Link from "next/link";

const navItems = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About Us" },
  { href: "/services", label: "Our Services" },
  { href: "/jobs", label: "Job Openings" },
  { href: "/contact", label: "Contact Us" },
  { href: "/upload-resume", label: "Upload Resume" },
] as const;

type SiteNavProps = {
  activeHref: (typeof navItems)[number]["href"];
};

export function SiteNav({ activeHref }: SiteNavProps) {
  return (
    <nav className="fixed top-0 z-50 w-full border-b border-white/10 bg-slate-900/60 backdrop-blur-xl shadow-2xl shadow-slate-950/40">
      <div className="mx-auto flex max-w-screen-2xl items-center justify-between px-6 py-4 md:px-12">
        <Link
          href="/"
          className="text-2xl font-bold tracking-tighter text-blue-100 uppercase"
        >
          Wenit Solutions
        </Link>

        <div className="hidden items-center gap-8 text-sm font-medium tracking-tight md:flex">
          {navItems.map((item) => {
            const isActive = item.href === activeHref;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={
                  isActive
                    ? "text-blue-200 border-b-2 border-amber-200/50 pb-1"
                    : "text-slate-300 hover:text-white transition-colors"
                }
              >
                {item.label}
              </Link>
            );
          })}
        </div>

        <Link
          href="/upload-resume"
          className="rounded-md bg-primary px-6 py-2.5 text-sm font-bold uppercase tracking-wider text-on-primary transition-all duration-300 ease-out hover:border-primary/20 hover:bg-white/5 hover:text-primary border border-transparent"
        >
          Upload Resume
        </Link>
      </div>
    </nav>
  );
}

