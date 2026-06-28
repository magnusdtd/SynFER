import React from "react";
import { Sliders, Info, Search } from "lucide-react";
import { EMOTION_PRESETS, FACS_ACTION_UNITS, Preset } from "../lib/constants";

interface SynthesisControllerProps {
  textPrompt: string;
  setTextPrompt: (prompt: string) => void;
  selectedFAUs: string[];
  setSelectedFAUs: (faus: string[]) => void;
  fauQuery: string;
  setFauQuery: (query: string) => void;
  activeFauCategory: string;
  setActiveFauCategory: (category: string) => void;
  triggerAlert: (type: "success" | "warning" | "error", text: string) => void;
}

export function SynthesisController({
  textPrompt,
  setTextPrompt,
  selectedFAUs,
  setSelectedFAUs,
  fauQuery,
  setFauQuery,
  activeFauCategory,
  setActiveFauCategory,
  triggerAlert
}: SynthesisControllerProps) {

  const applyPreset = (preset: Preset) => {
    setTextPrompt(preset.prompt);
    setSelectedFAUs(preset.faus);
    triggerAlert("success", `Applied preset: ${preset.name}`);
  };

  const selectAllCategoryFAUs = () => {
    const currentList = getFilteredFAUs();
    const currentIds = currentList.map(au => au.id);
    const missingIds = currentIds.filter(id => !selectedFAUs.includes(id));
    
    if (missingIds.length === 0) {
      setSelectedFAUs(selectedFAUs.filter(id => !currentIds.includes(id)));
    } else {
      setSelectedFAUs([...selectedFAUs, ...missingIds]);
    }
  };

  const clearAllSelectedFAUs = () => {
    setSelectedFAUs([]);
    triggerAlert("warning", "Cleared all facial action units.");
  };

  const getFilteredFAUs = () => {
    return FACS_ACTION_UNITS.filter(au => {
      const matchesCategory = activeFauCategory === "All" || au.category === activeFauCategory;
      const matchesSearch = au.id.toLowerCase().includes(fauQuery.toLowerCase()) || 
                            au.label.toLowerCase().includes(fauQuery.toLowerCase()) ||
                            au.description.toLowerCase().includes(fauQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  };

  const toggleFAU = (id: string) => {
    if (selectedFAUs.includes(id)) {
      setSelectedFAUs(selectedFAUs.filter(item => item !== id));
    } else {
      setSelectedFAUs([...selectedFAUs, id]);
    }
  };

  return (
    <section className="bg-zinc-900 border border-zinc-800 rounded-xl p-4 shadow-2xl flex flex-col gap-4 lg:col-span-1 lg:row-span-3 h-full overflow-hidden">
      {/* Action Header on Controls */}
      <div className="flex flex-col border-b border-zinc-800 pb-3 gap-3 flex-shrink-0">
        <div>
          <h2 className="text-xs font-semibold uppercase tracking-widest text-zinc-500 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-indigo-400" />
            Synthesis Controller Panel
          </h2>
          <p className="text-[11px] text-zinc-500 mt-0.5">Configure Action Units vectors with descriptions to target expression maps.</p>
        </div>
        
        {/* Quick Preset Selector */}
        <div className="flex flex-col gap-2 bg-zinc-950 p-2 rounded-lg border border-zinc-800/85">
          <span className="text-[9px] text-zinc-500 font-bold uppercase">Presets:</span>
          <div className="flex flex-row gap-2 overflow-x-auto custom-scrollbar pb-1">
            {EMOTION_PRESETS.map((preset) => (
              <button
                key={preset.name}
                type="button"
                id={`preset-btn-${preset.name.toLowerCase().replace(/\s+/g, '-')}`}
                title={preset.name}
                onClick={() => applyPreset(preset)}
                className="px-2 py-1 text-[10px] bg-zinc-900 border border-zinc-800 rounded hover:bg-zinc-800 hover:border-indigo-500/80 text-zinc-200 hover:text-white transition flex items-center gap-1.5 font-bold cursor-pointer active:scale-95 whitespace-nowrap shrink-0"
              >
                <span className="text-[11px] shrink-0">{preset.emoji}</span>
                <span className="text-[9px] uppercase tracking-wider font-bold text-center">{preset.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Component A - Text Prompt Input */}
      <div id="wrapper-component-a" className="flex flex-col gap-2 flex-shrink-0">
        <div className="flex items-end justify-between">
          <label className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
            High-level Character Description
          </label>
          <span className="text-[10px] text-zinc-600">
            {textPrompt.length} / 500
          </span>
        </div>
        
        <textarea
          id="text-prompt-box"
          rows={2}
          maxLength={500}
          placeholder="e.g., A young blonde woman with an angry expression..."
          value={textPrompt}
          onChange={(e) => setTextPrompt(e.target.value)}
          className="w-full bg-zinc-950 border border-zinc-800 rounded-lg p-3 text-sm text-zinc-200 placeholder:text-zinc-700 focus:outline-none focus:border-indigo-500/50 resize-none font-sans"
        />
        <p className="text-[10px] text-zinc-500 italic mt-0.5 flex items-center gap-1">
          <Info className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
          Describe ethnicity, gender, hair details...
        </p>
      </div>

      {/* Component B - FAU Selector Area */}
      <div id="wrapper-component-b" className="flex flex-col gap-3 flex-1 min-h-0">
        <div className="flex flex-col gap-2 flex-shrink-0">
          <div className="flex justify-between items-center w-full">
            <div className="flex items-center gap-2">
              <label className="text-xs font-semibold uppercase tracking-widest text-zinc-500">
                Facial Action Units
              </label>
              <span className="text-[10px] text-indigo-400 uppercase tracking-wider font-bold">
                {selectedFAUs.length} active
              </span>
            </div>
            
            {/* Sub-menu controllers */}
            <div className="flex items-center gap-2 shrink-0">
              <button
                type="button"
                onClick={selectAllCategoryFAUs}
                className="px-2 py-0.5 text-[9px] bg-zinc-950 border border-zinc-800 rounded text-zinc-400 hover:text-white hover:border-zinc-600 transition cursor-pointer font-bold uppercase tracking-wider"
              >
                All
              </button>
              <button
                type="button"
                onClick={clearAllSelectedFAUs}
                className="px-2 py-0.5 text-[9px] bg-zinc-950 border border-zinc-800 rounded text-zinc-400 hover:text-rose-450 hover:border-rose-900 transition cursor-pointer font-bold uppercase tracking-wider"
              >
                Clear
              </button>
            </div>
          </div>
        </div>

        {/* Categorization and Search bar row */}
        <div className="flex flex-col gap-2 bg-zinc-950 p-2 rounded-lg border border-zinc-800/85 flex-shrink-0">
          {/* Search Term Input */}
          <div className="relative">
            <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-zinc-500">
              <Search className="w-3.5 h-3.5" />
            </span>
            <input
              type="text"
              placeholder="Filter nodes..."
              value={fauQuery}
              onChange={(e) => setFauQuery(e.target.value)}
              className="w-full bg-zinc-900 border border-zinc-800 rounded pl-8 pr-3 py-1 text-xs text-zinc-200 placeholder-zinc-600 focus:outline-none focus:border-indigo-500/50"
            />
          </div>

          {/* Categories Tab selector */}
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-1">
            {["All", "Brows & Forehead", "Eyes & Eyelids", "Nose & Cheeks", "Lips & Mouth", "Jaw & Neck"].map(category => (
              <button
                key={category}
                type="button"
                onClick={() => setActiveFauCategory(category)}
                className={`px-1 py-1 text-[9px] font-sans font-bold uppercase tracking-wider rounded transition text-center truncate ${
                  activeFauCategory === category
                    ? "bg-indigo-600 text-white"
                    : "text-zinc-400 bg-zinc-900/60 hover:text-zinc-200 hover:bg-zinc-900"
                }`}
                title={category}
              >
                {category.split(" ")[0]}
              </button>
            ))}
          </div>
        </div>

        {/* Grid block of 41 toggle chips */}
        <div className="bg-zinc-950 p-2 rounded-lg border border-zinc-800/85 flex-1 min-h-0 overflow-y-auto custom-scrollbar">
          <div className="grid grid-cols-2 lg:grid-cols-3 gap-1">
            {getFilteredFAUs().map((au) => {
              const isSelected = selectedFAUs.includes(au.id);
              return (
                <button
                  key={au.id}
                  type="button"
                  id={`au-toggle-${au.id.toLowerCase()}`}
                  onClick={() => toggleFAU(au.id)}
                  className={`px-1.5 py-1 rounded text-[9px] flex items-center justify-between transition cursor-pointer select-none ${
                    isSelected
                      ? "bg-indigo-600 text-white shadow-lg shadow-indigo-900/20"
                      : "bg-zinc-900 border border-zinc-800 text-zinc-400 hover:border-zinc-600"
                  }`}
                  title={au.description}
                >
                  <div className="flex items-center gap-1 truncate mr-1">
                    <span className={`${isSelected ? "text-indigo-200" : "text-indigo-400"} font-semibold shrink-0`}>
                      {au.id}
                    </span>
                    <span className="truncate font-semibold text-[9px]">
                      {au.label.replace(" Raiser", "").replace(" Lowerer", "").replace(" Tightener", "").replace(" Depressor", "").replace(" Puller", "").replace(" Wrinkler", "")}
                    </span>
                  </div>
                  {isSelected && (
                    <div className="w-1.5 h-1.5 rounded-full bg-white animate-pulse shrink-0 ml-1"></div>
                  )}
                </button>
              );
            })}
          </div>
          {getFilteredFAUs().length === 0 && (
            <div className="text-center py-4 text-xs text-zinc-500 italic">
              No nodes found.
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
