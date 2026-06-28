import React from "react";
import Image from "next/image";
import { Camera, Sparkles } from "lucide-react";
import { motion } from "motion/react";

interface SynthesisCanvasProps {
  generatedImageSrc: string | null;
  isLoading: boolean;
  synthesisMetadata: any;
  selectedFAUs: string[];
}

export function SynthesisCanvas({
  generatedImageSrc,
  isLoading,
  synthesisMetadata,
  selectedFAUs,
}: SynthesisCanvasProps) {
  return (
    <section className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-2xl relative overflow-hidden flex flex-col justify-center lg:col-span-1 lg:row-span-2 h-full">
      {/* Tech Background Grid Graphics */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#18181b_1px,transparent_1px),linear-gradient(to_bottom,#18181b_1px,transparent_1px)] bg-[size:24px_24px] opacity-40 pointer-events-none" />
      
      <div className="flex-1 flex flex-col z-10 relative">
        {/* Header section on card */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-ping" />
            <span className="text-[10px] uppercase text-zinc-400 tracking-widest font-bold">
              SYNFER CANVAS STAGE
            </span>
          </div>
          
          <div className="flex items-center gap-2">
            <div className="text-[9px] bg-indigo-900/30 text-indigo-400 px-2 py-0.5 rounded border border-indigo-500/30 font-bold tracking-widest">READY</div>
          </div>
        </div>

        {/* Main Image Stage Box */}
        <div className="relative w-full flex-1 rounded-xl bg-zinc-950 overflow-hidden border border-zinc-800 shadow-inner flex items-center justify-center min-h-[300px] mt-auto mb-auto">
          
          {/* 1. Empty/Initial State */}
          {!generatedImageSrc && !isLoading && (
            <div className="flex flex-col items-center justify-center text-center p-8 z-10 relative">
              <div className="w-20 h-20 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center mb-4 text-zinc-600">
                <Camera className="w-10 h-10 animate-pulse" />
              </div>
              <h3 className="text-zinc-100 text-xs font-bold tracking-widest uppercase">
                No synthesized face yet
              </h3>
              <p className="text-[11px] text-zinc-500 max-w-xs mt-2 italic lowercase">
                Your synthesized expression will appear here.
              </p>
            </div>
          )}

          {/* 2. Success Content State */}
          {generatedImageSrc && (
            <div className="absolute inset-0 w-full h-full">
              <Image
                src={generatedImageSrc}
                alt="Synthesized Emotional Expression Face Portrait"
                fill
                className={`object-cover transition-all duration-300 ${
                  isLoading ? "blur-md scale-95 opacity-50" : "blur-0 scale-100 opacity-100"
                }`}
                referrerPolicy="no-referrer"
              />

            </div>
          )}

          {/* 3. Loading overlay state */}
          {isLoading && (
            <div className="absolute inset-0 bg-zinc-950/85 backdrop-blur-sm z-30 flex flex-col items-center justify-center p-6 text-center">
              <div className="relative mb-4 flex items-center justify-center">
                <div className="w-16 h-16 rounded-full border-4 border-indigo-950 border-t-indigo-500 animate-spin" />
                <Sparkles className="w-6 h-6 text-indigo-400 absolute animate-pulse" />
              </div>
              <h3 className="font-bold text-sm tracking-wide text-indigo-300 animate-pulse">
                Synthesizing Action Units...
              </h3>
              <p className="text-xs text-zinc-400 max-w-xs mt-2 font-semibold">
                Target express vectors: {selectedFAUs.join(", ") || "None"}
              </p>
              {/* Simulated progress meters */}
              <div className="w-48 bg-zinc-900 h-1 rounded-full overflow-hidden mt-4 border border-zinc-800">
                <motion.div 
                  initial={{ x: "-100%" }} 
                  animate={{ x: "100%" }} 
                  transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }} 
                  className="bg-gradient-to-r from-transparent via-indigo-400 to-transparent w-1/2 h-full"
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
