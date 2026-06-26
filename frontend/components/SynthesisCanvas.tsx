import React from "react";
import Image from "next/image";
import { Camera, Sparkles } from "lucide-react";
import { motion } from "motion/react";

interface SynthesisCanvasProps {
  generatedImageSrc: string | null;
  isLoading: boolean;
  showLandmarks: boolean;
  setShowLandmarks: (show: boolean) => void;
  synthesisMetadata: any;
  selectedFAUs: string[];
}

export function SynthesisCanvas({
  generatedImageSrc,
  isLoading,
  showLandmarks,
  setShowLandmarks,
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
            {generatedImageSrc && (
              <label className="flex items-center gap-1.5 cursor-pointer select-none mr-2">
                <input 
                  type="checkbox"
                  checked={showLandmarks}
                  onChange={() => setShowLandmarks(!showLandmarks)}
                  className="sr-only"
                />
                <span className={`w-8 h-4 rounded-full transition-colors relative flex items-center ${
                  showLandmarks ? "bg-indigo-600" : "bg-zinc-700"
                }`}>
                  <span className={`w-3 h-3 rounded-full bg-white transition-all absolute ${
                    showLandmarks ? "right-0.5" : "left-0.5"
                  }`} />
                </span>
                <span className="text-[10px] text-zinc-400 font-semibold uppercase tracking-widest">Landmarks</span>
              </label>
            )}
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

              {/* Interactive high-tech simulated vector coordinates mapping overlays */}
              {showLandmarks && synthesisMetadata?.landmarks && !isLoading && (
                <svg className="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 400 400" preserveAspectRatio="xMidYMid slice">
                  {/* Eyebrows */}
                  <path 
                    d={`M ${synthesisMetadata.landmarks.leftBrow.map((p: any) => `${p.x} ${p.y}`).join(" L ")}`} 
                    fill="none" stroke="#6366f1" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="3,3" className="opacity-80"
                  />
                  <path 
                    d={`M ${synthesisMetadata.landmarks.rightBrow.map((p: any) => `${p.x} ${p.y}`).join(" L ")}`} 
                    fill="none" stroke="#6366f1" strokeWidth="2.5" strokeLinecap="round" strokeDasharray="3,3" className="opacity-80"
                  />
                  
                  {/* Eyes */}
                  <path 
                    d={`M ${synthesisMetadata.landmarks.leftEye.map((p: any) => `${p.x} ${p.y}`).join(" L ")} Z`} 
                    fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" className="opacity-90"
                  />
                  <path 
                    d={`M ${synthesisMetadata.landmarks.rightEye.map((p: any) => `${p.x} ${p.y}`).join(" L ")} Z`} 
                    fill="none" stroke="#10b981" strokeWidth="2" strokeLinecap="round" className="opacity-90"
                  />

                  {/* Nose */}
                  <path 
                    d={`M ${synthesisMetadata.landmarks.noseBridge.map((p: any) => `${p.x} ${p.y}`).join(" L ")} M ${synthesisMetadata.landmarks.noseTip.map((p: any) => `${p.x} ${p.y}`).join(" L ")}`} 
                    fill="none" stroke="#f59e0b" strokeWidth="2" strokeLinecap="round" className="opacity-80"
                  />

                  {/* Mouth */}
                  <path 
                    d={`M ${synthesisMetadata.landmarks.mouthOuter.map((p: any) => `${p.x} ${p.y}`).join(" L ")} Z`} 
                    fill="none" stroke="#6366f1" strokeWidth="3" strokeLinecap="round" className="opacity-100"
                  />

                  {/* Jaw */}
                  <path 
                    d={`M ${synthesisMetadata.landmarks.jaw.map((p: any) => `${p.x} ${p.y}`).join(" L ")}`} 
                    fill="none" stroke="#e4e4e7" strokeWidth="1.5" strokeLinecap="round" strokeDasharray="5,3" className="opacity-50"
                  />

                  {/* Node Dots map */}
                  {[
                    ...synthesisMetadata.landmarks.leftBrow,
                    ...synthesisMetadata.landmarks.rightBrow,
                    ...synthesisMetadata.landmarks.leftEye,
                    ...synthesisMetadata.landmarks.rightEye,
                    ...synthesisMetadata.landmarks.noseTip,
                    ...synthesisMetadata.landmarks.mouthOuter,
                    ...synthesisMetadata.landmarks.jaw
                  ].map((pt: any, idx: number) => (
                    <g key={idx}>
                      <circle 
                        cx={pt.x} 
                        cy={pt.y} 
                        r="3.5" 
                        className={`fill-[#10b981] stroke-zinc-950 stroke-[1.5] ${
                          idx % 4 === 0 ? "animate-pulse fill-indigo-400 r-5" : ""
                        }`}
                      />
                      {idx % 7 === 0 && (
                        <text 
                          x={pt.x + 6} 
                          y={pt.y + 3} 
                          className="fill-indigo-300 text-[8px] opacity-75 font-bold"
                        >
                          v{idx}
                        </text>
                      )}
                    </g>
                  ))}
                </svg>
              )}
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
