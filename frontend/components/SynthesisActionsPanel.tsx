import React from "react";
import { Sliders, RefreshCw, Download, Trash2 } from "lucide-react";

interface SynthesisActionsPanelProps {
  synthesisMetadata: any;
  isLoading: boolean;
  generatedImageSrc: string | null;
  handleDownloadImage: () => void;
  handleClearAll: () => void;
}

export function SynthesisActionsPanel({
  synthesisMetadata,
  isLoading,
  generatedImageSrc,
  handleDownloadImage,
  handleClearAll,
}: SynthesisActionsPanelProps) {
  return (
    <section className="bg-zinc-900 border border-zinc-800 rounded-xl p-3 shadow-2xl flex flex-col md:flex-row gap-4 lg:col-span-2 lg:row-span-1 items-center h-full">
      {/* Metadata (Left side) */}
      <div className="flex-1 bg-zinc-950 p-4 rounded-xl border border-zinc-800/80 z-10 w-full h-full flex flex-col justify-center">
        <h4 className="text-[10px] text-zinc-400 uppercase tracking-wider mb-2.5 font-bold flex items-center gap-1.5">
          <Sliders className="w-3.5 h-3.5 text-indigo-400" />
          Synthesis Render Metadata
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-x-4 gap-y-2 text-[11px] font-medium">
          <div>
            <span className="text-zinc-500">Expression State:</span>
            <p className="text-indigo-400 font-bold capitalize mt-0.5">
              {synthesisMetadata?.expressionDetected || "Awaiting Synthesis"}
            </p>
          </div>
          <div>
            <span className="text-zinc-500">Engine Confidence:</span>
            <p className="text-zinc-300 mt-0.5">
              {synthesisMetadata ? `${(synthesisMetadata.confidence * 100).toFixed(1)}%` : "0.0%"}
            </p>
          </div>
          <div>
            <span className="text-zinc-500">Render Time:</span>
            <p className="text-zinc-300 mt-0.5">
              {synthesisMetadata ? `${synthesisMetadata.renderingTimeMs} ms` : "0 ms"}
            </p>
          </div>
        </div>
      </div>

      {/* Actions (Right side) */}
      <div className="flex flex-col gap-3 w-full md:w-[300px] shrink-0">
        <button
          type="submit"
          id="btn-generate-expression"
          disabled={isLoading}
          className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-xl shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all flex items-center justify-center gap-3 active:scale-[0.98] cursor-pointer disabled:bg-zinc-850 disabled:cursor-not-allowed disabled:border-zinc-800 disabled:shadow-none"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-4.5 h-4.5 animate-spin text-white" />
              <span className="uppercase tracking-[0.2em] text-xs font-bold">Synthesizing...</span>
            </>
          ) : (
            <>
              <span className="uppercase tracking-[0.2em] text-sm">Generate Expression</span>
              <svg className="w-5 h-5 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            </>
          )}
        </button>

        <div className={`flex gap-2 transition-all duration-300 ${generatedImageSrc ? 'opacity-100 h-10' : 'opacity-0 h-0 overflow-hidden mt-[-12px]'}`}>
          <button
            type="button"
            onClick={handleDownloadImage}
            className="flex-1 py-2 bg-zinc-900 hover:bg-zinc-800 text-zinc-300 rounded-lg text-xs font-medium border border-zinc-800 flex items-center justify-center gap-2 transition cursor-pointer"
          >
            <Download className="w-4 h-4 text-indigo-400" />
            Download
          </button>
          <button
            type="button"
            onClick={handleClearAll}
            title="Clear All Inputs and Stage"
            className="px-4 rounded-lg bg-zinc-950 border border-zinc-800 hover:bg-zinc-900 text-zinc-400 hover:text-rose-400 transition cursor-pointer"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
        
      </div>
    </section>
  );
}
