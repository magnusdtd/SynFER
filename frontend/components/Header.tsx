import React from "react";
import { Camera, Github } from "lucide-react";

export function Header() {
  return (
    <header id="synfer-header" className="flex items-center justify-between px-6 py-3 border-b border-zinc-800 bg-zinc-900/50 sticky top-0 z-40 backdrop-blur-md">
      <div className="max-w-[1600px] mx-auto w-full flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-indigo-600 rounded flex items-center justify-center">
            <Camera className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5 font-sans">
                SynFER <span className="text-zinc-500 font-normal text-sm ml-0.5"> Facial Expression Synthesis Engine</span>
              </h1>
            </div>
            <p className="text-[11px] text-zinc-500 font-sans mt-0.5">
              Facial expression synthesis via high-level descriptors & action unit coordinates mapping
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <div className="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-full flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></span>
            <span className="text-[10px] font-bold text-emerald-500 uppercase tracking-widest">API LIVE</span>
          </div>
          <a
            href="https://github.com/magnusdtd/SynFER"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-zinc-950/50 hover:bg-zinc-800 text-zinc-400 hover:text-zinc-200 p-2 rounded-lg border border-zinc-800/50 transition-colors flex items-center justify-center"
            title="GitHub Repo"
          >
            <Github className="w-4 h-4" />
          </a>
        </div>
      </div>
    </header>
  );
}
