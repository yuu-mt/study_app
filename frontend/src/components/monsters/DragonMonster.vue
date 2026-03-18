<template>
    <!-- stage 0: たまご -->
    <g v-if="stage === 0">
        <defs>
        <radialGradient id="dragonEgg" cx="38%" cy="35%">
            <stop offset="0%" stop-color="#fecaca"/>
            <stop offset="100%" stop-color="#f87171"/>
        </radialGradient>
        </defs>
        <ellipse cx="60" cy="78" rx="38" ry="48" fill="url(#dragonEgg)" stroke="#fca5a5" stroke-width="1.5" style="animation: wobble 2s ease-in-out infinite"/>
        <ellipse cx="46" cy="60" rx="12" ry="8" fill="white" opacity="0.5"/>
        <ellipse cx="72" cy="85" rx="6" ry="4" fill="#f87171" opacity="0.2" transform="rotate(-20 72 85)"/>
        <ellipse cx="52" cy="94" rx="5" ry="3" fill="#f87171" opacity="0.15" transform="rotate(15 52 94)"/>
    </g>

    <!-- stage 1: ちびドラゴン -->
    <g v-else-if="stage === 1">
        <circle cx="60" cy="72" r="30" fill="#f87171"/>
        <ellipse cx="60" cy="82" rx="18" ry="14" fill="#fef3c7" opacity="0.8"/>
        <ellipse cx="38" cy="46" rx="8" ry="11" fill="#fca5a5" transform="rotate(-15 38 46)"/>
        <ellipse cx="38" cy="47" rx="5" ry="7" fill="#fee2e2" transform="rotate(-15 38 47)"/>
        <ellipse cx="82" cy="46" rx="8" ry="11" fill="#fca5a5" transform="rotate(15 82 46)"/>
        <ellipse cx="82" cy="47" rx="5" ry="7" fill="#fee2e2" transform="rotate(15 82 47)"/>
        <circle cx="50" cy="68" r="9" fill="white"/>
        <circle cx="70" cy="68" r="9" fill="white"/>
        <circle cx="51" cy="69" r="5" fill="#7f1d1d"/>
        <circle cx="71" cy="69" r="5" fill="#7f1d1d"/>
        <circle cx="52" cy="67" r="2" fill="white"/>
        <circle cx="72" cy="67" r="2" fill="white"/>
        <circle cx="52" cy="80" r="3" fill="#ef4444"/>
        <circle cx="68" cy="80" r="3" fill="#ef4444"/>
        <path d="M50 86 Q60 94 70 86" fill="none" stroke="#991b1b" stroke-width="2" stroke-linecap="round"/>
        <ellipse cx="38" cy="76" rx="7" ry="5" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="82" cy="76" rx="7" ry="5" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="36" cy="96" rx="12" ry="8" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="84" cy="96" rx="12" ry="8" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="50" cy="106" rx="10" ry="7" fill="#f87171"/>
        <ellipse cx="70" cy="106" rx="10" ry="7" fill="#f87171"/>
    </g>

    <!-- stage 2: こドラゴン -->
    <g v-else-if="stage === 2">
        <path d="M88 118 Q112 104 108 80 Q104 60 92 70" fill="none" stroke="#fca5a5" stroke-width="10" stroke-linecap="round"/>
        <polygon points="92,70 104,58 96,74" fill="#fecaca"/>
        <ellipse cx="58" cy="108" rx="46" ry="46" fill="#f87171"/>
        <ellipse cx="58" cy="116" rx="30" ry="32" fill="#fef3c7" opacity="0.7"/>
        <path d="M16 92 Q-4 62 12 48 Q26 55 30 80" fill="#fca5a5" opacity="0.85"/>
        <path d="M100 92 Q120 62 104 48 Q90 55 86 80" fill="#fca5a5" opacity="0.85"/>
        <circle cx="58" cy="58" r="32" fill="#f87171"/>
        <ellipse cx="36" cy="30" rx="10" ry="13" fill="#fca5a5" transform="rotate(-20 36 30)"/>
        <ellipse cx="36" cy="31" rx="6" ry="8" fill="#fee2e2" transform="rotate(-20 36 31)"/>
        <ellipse cx="80" cy="30" rx="10" ry="13" fill="#fca5a5" transform="rotate(20 80 30)"/>
        <ellipse cx="80" cy="31" rx="6" ry="8" fill="#fee2e2" transform="rotate(20 80 31)"/>
        <circle cx="46" cy="54" r="11" fill="white"/>
        <circle cx="70" cy="54" r="11" fill="white"/>
        <circle cx="47" cy="55" r="7" fill="#7f1d1d"/>
        <circle cx="71" cy="55" r="7" fill="#7f1d1d"/>
        <circle cx="49" cy="53" r="2.5" fill="white"/>
        <circle cx="73" cy="53" r="2.5" fill="white"/>
        <path d="M44 66 Q58 76 72 66" fill="none" stroke="#991b1b" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="32" cy="66" rx="8" ry="5" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="84" cy="66" rx="8" ry="5" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="44" cy="148" rx="12" ry="8" fill="#f87171"/>
        <ellipse cx="72" cy="148" rx="12" ry="8" fill="#f87171"/>
    </g>

    <!-- stage 3: ドラゴン -->
    <g v-else-if="stage === 3">
        <path d="M90 122 Q118 106 114 80 Q110 58 96 68" fill="none" stroke="#fca5a5" stroke-width="12" stroke-linecap="round"/>
        <polygon points="96,68 110,54 102,72" fill="#fecaca"/>
        <ellipse cx="58" cy="110" rx="50" ry="50" fill="#ef4444"/>
        <ellipse cx="58" cy="120" rx="34" ry="36" fill="#fef3c7" opacity="0.65"/>
        <path d="M8 95 Q-16 60 4 42 Q22 50 26 82" fill="#fca5a5" opacity="0.9"/>
        <path d="M108 95 Q132 60 112 42 Q94 50 90 82" fill="#fca5a5" opacity="0.9"/>
        <ellipse cx="58" cy="56" rx="36" ry="34" fill="#ef4444"/>
        <ellipse cx="32" cy="24" rx="12" ry="16" fill="#fca5a5" transform="rotate(-20 32 24)"/>
        <ellipse cx="32" cy="25" rx="7" ry="10" fill="#fee2e2" transform="rotate(-20 32 25)"/>
        <ellipse cx="84" cy="24" rx="12" ry="16" fill="#fca5a5" transform="rotate(20 84 24)"/>
        <ellipse cx="84" cy="25" rx="7" ry="10" fill="#fee2e2" transform="rotate(20 84 25)"/>
        <circle cx="44" cy="52" r="13" fill="white"/>
        <circle cx="72" cy="52" r="13" fill="white"/>
        <circle cx="45" cy="53" r="8" fill="#7f1d1d"/>
        <circle cx="73" cy="53" r="8" fill="#7f1d1d"/>
        <circle cx="47" cy="51" r="3" fill="white"/>
        <circle cx="75" cy="51" r="3" fill="white"/>
        <path d="M42 68 Q58 80 74 68" fill="none" stroke="#991b1b" stroke-width="3" stroke-linecap="round"/>
        <polygon points="48,70 46,80 52,78" fill="white"/>
        <polygon points="68,70 70,80 64,78" fill="white"/>
        <ellipse cx="28" cy="68" rx="10" ry="6" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="88" cy="68" rx="10" ry="6" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="42" cy="154" rx="14" ry="9" fill="#ef4444"/>
        <ellipse cx="74" cy="154" rx="14" ry="9" fill="#ef4444"/>
    </g>

    <!-- stage 4: 伝説のドラゴン -->
    <g v-else>
        <defs>
        <radialGradient id="fireGrad" cx="50%" cy="0%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="40%" stop-color="#fef08a"/>
            <stop offset="80%" stop-color="#f97316"/>
            <stop offset="100%" stop-color="#dc2626" stop-opacity="0"/>
        </radialGradient>
        </defs>
        <ellipse cx="58" cy="16" rx="10" ry="18" fill="url(#fireGrad)" style="animation: flicker 0.8s ease-in-out infinite alternate"/>
        <ellipse cx="40" cy="22" rx="6" ry="11" fill="url(#fireGrad)" style="animation: flicker 0.8s ease-in-out infinite alternate; animation-delay: 0.3s"/>
        <ellipse cx="76" cy="22" rx="6" ry="11" fill="url(#fireGrad)" style="animation: flicker 0.8s ease-in-out infinite alternate; animation-delay: 0.6s"/>
        <path d="M92 126 Q122 108 118 82 Q114 58 98 70" fill="none" stroke="#fca5a5" stroke-width="14" stroke-linecap="round"/>
        <polygon points="98,70 114,54 106,74" fill="#fecaca"/>
        <ellipse cx="58" cy="114" rx="52" ry="52" fill="#dc2626"/>
        <ellipse cx="58" cy="126" rx="36" ry="38" fill="#fef9c3" opacity="0.6"/>
        <path d="M4 98 Q-22 58 2 38 Q22 48 24 84" fill="#fca5a5" opacity="0.95"/>
        <path d="M112 98 Q138 58 114 38 Q94 48 92 84" fill="#fca5a5" opacity="0.95"/>
        <ellipse cx="58" cy="58" rx="38" ry="36" fill="#dc2626"/>
        <ellipse cx="28" cy="24" rx="13" ry="18" fill="#fca5a5" transform="rotate(-20 28 24)"/>
        <ellipse cx="28" cy="25" rx="8" ry="11" fill="#fee2e2" transform="rotate(-20 28 25)"/>
        <ellipse cx="88" cy="24" rx="13" ry="18" fill="#fca5a5" transform="rotate(20 88 24)"/>
        <ellipse cx="88" cy="25" rx="8" ry="11" fill="#fee2e2" transform="rotate(20 88 25)"/>
        <circle cx="42" cy="54" r="15" fill="white"/>
        <circle cx="74" cy="54" r="15" fill="white"/>
        <circle cx="43" cy="55" r="9" fill="#fbbf24"/>
        <circle cx="75" cy="55" r="9" fill="#fbbf24"/>
        <circle cx="43" cy="55" r="5" fill="#7f1d1d"/>
        <circle cx="75" cy="55" r="5" fill="#7f1d1d"/>
        <circle cx="45" cy="53" r="2" fill="white"/>
        <circle cx="77" cy="53" r="2" fill="white"/>
        <path d="M40 72 Q58 86 76 72" fill="none" stroke="#991b1b" stroke-width="3" stroke-linecap="round"/>
        <polygon points="46,74 44,86 50,83" fill="white"/>
        <polygon points="70,74 72,86 66,83" fill="white"/>
        <ellipse cx="26" cy="72" rx="11" ry="7" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="90" cy="72" rx="11" ry="7" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="40" cy="160" rx="15" ry="10" fill="#dc2626"/>
        <ellipse cx="76" cy="160" rx="15" ry="10" fill="#dc2626"/>
    </g>
</template>

<script setup>
defineProps({ stage: { type: Number, default: 0 } })
</script>