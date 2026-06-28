export interface FAU {
  id: string;
  label: string;
  description: string;
  category: "Brows & Forehead" | "Eyes & Eyelids" | "Nose & Cheeks" | "Lips & Mouth" | "Jaw & Neck";
}

export const FACS_ACTION_UNITS: FAU[] = [
  // Brows & Forehead
  { id: "AU1", label: "Inner Brow Raiser", description: "Raises the inner corner of the eyebrows.", category: "Brows & Forehead" },
  { id: "AU2", label: "Outer Brow Raiser", description: "Raises the outer corner of the eyebrows.", category: "Brows & Forehead" },
  { id: "AU4", label: "Brow Lowerer", description: "Draws eyebrows together and downward.", category: "Brows & Forehead" },
  { id: "AU41", label: "Glabella Furrow", description: "Vertical furrows between the eyebrows.", category: "Brows & Forehead" },

  // Eyes & Eyelids
  { id: "AU5", label: "Upper Lid Raiser", description: "Widens the eye, exposing the sclera.", category: "Eyes & Eyelids" },
  { id: "AU6", label: "Cheek Raiser", description: "Lifts the cheek, narrows eye aperture.", category: "Eyes & Eyelids" },
  { id: "AU7", label: "Lid Tightener", description: "Tightens the lower eyelid.", category: "Eyes & Eyelids" },
  { id: "AU42", label: "Eyelid Slit", description: "Narrows the eye spacing significantly.", category: "Eyes & Eyelids" },
  { id: "AU43", label: "Eyes Closed", description: "Closes both eyes completely.", category: "Eyes & Eyelids" },
  { id: "AU44", label: "Squint", description: "Tenses the eyelid sphincter muscles.", category: "Eyes & Eyelids" },
  { id: "AU45", label: "Blink", description: "Brief closure of both eyelids.", category: "Eyes & Eyelids" },
  { id: "AU46", label: "Wink", description: "Asymmetric closure of one eye.", category: "Eyes & Eyelids" },
  { id: "AU61", label: "Eyes Left", description: "Directs gaze toward the left side.", category: "Eyes & Eyelids" },

  // Nose & Cheeks
  { id: "AU9", label: "Nose Wrinkler", description: "Wrinkles the skin over the nose bridge.", category: "Nose & Cheeks" },
  { id: "AU11", label: "Nasolabial Deepener", description: "Deepens the crease from nose to mouth.", category: "Nose & Cheeks" },
  { id: "AU14", label: "Dimpler", description: "Gives puffiness and dimples to the cheeks.", category: "Nose & Cheeks" },
  { id: "AU38", label: "Nostril Dilator", description: "Flares the nostrils outwards.", category: "Nose & Cheeks" },
  { id: "AU39", label: "Nostril Compressor", description: "Squeezes the nostrils inwards.", category: "Nose & Cheeks" },

  // Lips & Mouth
  { id: "AU10", label: "Upper Lip Raiser", description: "Raises the center of the upper lip.", category: "Lips & Mouth" },
  { id: "AU12", label: "Lip Corner Puller", description: "Pulls lips corner up and back (Smile).", category: "Lips & Mouth" },
  { id: "AU13", label: "Sharp Lip Puller", description: "Sharp upward tug of lip muscles.", category: "Lips & Mouth" },
  { id: "AU15", label: "Lip Corner Depressor", description: "Pulls mouth corners down (Frown).", category: "Lips & Mouth" },
  { id: "AU16", label: "Lower Lip Depressor", description: "Pulls the lower lip downward.", category: "Lips & Mouth" },
  { id: "AU18", label: "Lip Puckerer", description: "Tightens mouth and purses lips outward.", category: "Lips & Mouth" },
  { id: "AU20", label: "Lip Stretcher", description: "Stretches the mouth horizontally.", category: "Lips & Mouth" },
  { id: "AU22", label: "Lip Funneler", description: "Shapes mouth for vocalization.", category: "Lips & Mouth" },
  { id: "AU23", label: "Lip Tightener", description: "Flattens and tightens lips borders.", category: "Lips & Mouth" },
  { id: "AU24", label: "Lip Presser", description: "Presses lips together firmly.", category: "Lips & Mouth" },
  { id: "AU25", label: "Lips Part", description: "Separates the upper and lower lips.", category: "Lips & Mouth" },
  { id: "AU27", label: "Mouth Stretch", description: "Pulls mouth wide open.", category: "Lips & Mouth" },
  { id: "AU28", label: "Lip Suck", description: "Sucks the lips in over teeth.", category: "Lips & Mouth" },

  // Jaw & Neck
  { id: "AU17", label: "Chin Raiser", description: "Lifts the chin boss, wrinkles chin skin.", category: "Jaw & Neck" },
  { id: "AU26", label: "Jaw Drop", description: "Relaxes muscles letting jaw hang low.", category: "Jaw & Neck" },
  { id: "AU31", label: "Jaw Clencher", description: "Grinds/clenches the jaw teeth.", category: "Jaw & Neck" },
  { id: "AU32", label: "Lip Biter", description: "Clamps lower lip under dental line.", category: "Jaw & Neck" },
  { id: "AU33", label: "Cheek Blow", description: "Inflates cheeks with compressed air.", category: "Jaw & Neck" },
  { id: "AU34", label: "Cheek Suck", description: "Draws cheeks inward symmetrically.", category: "Jaw & Neck" },
  { id: "AU35", label: "Cheek Pouch", description: "Protrudes side-cheek muscle pockets.", category: "Jaw & Neck" },
  { id: "AU36", label: "Tongue Show", description: "Pushes tongue past outer lip boundary.", category: "Jaw & Neck" },
  { id: "AU37", label: "Lip Wipe", description: "Sideways wiping motion of oral seal.", category: "Jaw & Neck" },
  { id: "AU51", label: "Head Left", description: "Simulates rotation tracking to the left.", category: "Jaw & Neck" },
  { id: "AU52", label: "Head Right", description: "Simulates rotation tracking to the right.", category: "Jaw & Neck" }
];

export interface Preset {
  name: string;
  faus: string[];
  prompt: string;
  emoji: string;
}

export const EMOTION_PRESETS: Preset[] = [
  {
    name: "Pure Happiness",
    faus: ["AU6", "AU12", "AU25"],
    prompt: "An elegant young woman with a radiant happy smile, warm crinkled eyes, looking directly into the camera with absolute joy.",
    emoji: "😊"
  },
  {
    name: "Intense Anger",
    faus: ["AU4", "AU5", "AU7", "AU23", "AU24"],
    prompt: "A close-up portrait of a stern-faced woman with deeply furrowed eyebrows, flared nostrils, and a highly intense furious glare.",
    emoji: "😠"
  },
  {
    name: "Shock & Surprise",
    faus: ["AU1", "AU2", "AU5", "AU26", "AU27"],
    prompt: "A portrait of a person showing extreme astonishment, with eyebrows raised high, eyes wide shut-open, and mouth wide open in surprise.",
    emoji: "😲"
  },
  {
    name: "Melancholic Sadness",
    faus: ["AU1", "AU4", "AU15", "AU17"],
    prompt: "A moody cinematic photo of someone with downcast eyes, trembling inner brow, and a subtle frown full of sorrow and raw emotion.",
    emoji: "😢"
  },
  {
    name: "Disgusted Scorn",
    faus: ["AU9", "AU10", "AU17"],
    prompt: "A male face with a highly expressive snarl of disgust, nose wrinkled up, and upper lip raised in extreme distaste.",
    emoji: "🤢"
  }
];
