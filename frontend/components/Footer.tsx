import React from "react";

export function Footer() {
  return (
    <footer id="synfer-footer" className="px-6 py-2 bg-zinc-950 border-t border-zinc-900 flex flex-col md:flex-row justify-between items-center text-[10px] text-zinc-600 gap-4 max-w-[1600px] w-full mx-auto">
      <div className="flex gap-4">
        <span>Made by magnusdtd</span>
      </div>
      <div className="font-semibold uppercase">
        © 2026 SYNTHETIC FACIAL RESEARCH
      </div>
    </footer>
  );
}
