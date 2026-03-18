<template>
    <!-- stage 0: たまご -->
    <g v-if="stage === 0">
        <defs>
        <radialGradient id="slimeEgg" cx="38%" cy="35%">
            <stop offset="0%" stop-color="#bae6fd"/>
            <stop offset="100%" stop-color="#38bdf8"/>
        </radialGradient>
        </defs>
        <ellipse cx="60" cy="78" rx="38" ry="48" fill="url(#slimeEgg)" stroke="#7dd3fc" stroke-width="1.5" style="animation: wobble 2s ease-in-out infinite"/>
        <ellipse cx="46" cy="60" rx="12" ry="8" fill="white" opacity="0.5"/>
        <ellipse cx="72" cy="85" rx="6" ry="4" fill="#38bdf8" opacity="0.2" transform="rotate(-20 72 85)"/>
        <ellipse cx="52" cy="94" rx="5" ry="3" fill="#38bdf8" opacity="0.15" transform="rotate(15 52 94)"/>
    </g>

    <!-- stage 1: ちびスライム -->
    <g v-else-if="stage === 1">
        <ellipse cx="60" cy="88" rx="34" ry="30" fill="#7dd3fc"/>
        <ellipse cx="60" cy="100" rx="34" ry="22" fill="#38bdf8"/>
        <ellipse cx="48" cy="72" rx="8" ry="6" fill="white" opacity="0.6"/>
        <circle cx="50" cy="82" r="7" fill="white"/>
        <circle cx="70" cy="82" r="7" fill="white"/>
        <circle cx="51" cy="83" r="4" fill="#1e3a5f"/>
        <circle cx="71" cy="83" r="4" fill="#1e3a5f"/>
        <circle cx="52" cy="82" r="1.5" fill="white"/>
        <circle cx="72" cy="82" r="1.5" fill="white"/>
        <path d="M52 92 Q60 98 68 92" fill="none" stroke="#1e3a5f" stroke-width="2" stroke-linecap="round"/>
        <line x1="50" y1="58" x2="46" y2="44" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="46" cy="44" r="4" fill="#7dd3fc"/>
        <line x1="70" y1="58" x2="74" y2="44" stroke="#38bdf8" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="74" cy="44" r="4" fill="#7dd3fc"/>
    </g>

    <!-- stage 2: スライム -->
    <g v-else-if="stage === 2">
        <ellipse cx="60" cy="85" rx="44" ry="40" fill="#38bdf8"/>
        <ellipse cx="60" cy="100" rx="44" ry="30" fill="#0ea5e9"/>
        <ellipse cx="44" cy="65" rx="14" ry="10" fill="white" opacity="0.5"/>
        <circle cx="46" cy="78" r="10" fill="white"/>
        <circle cx="74" cy="78" r="10" fill="white"/>
        <circle cx="47" cy="79" r="6" fill="#0c4a6e"/>
        <circle cx="75" cy="79" r="6" fill="#0c4a6e"/>
        <circle cx="49" cy="77" r="2" fill="white"/>
        <circle cx="77" cy="77" r="2" fill="white"/>
        <path d="M48 92 Q60 102 72 92" fill="none" stroke="#0c4a6e" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="34" cy="90" rx="7" ry="5" fill="#bae6fd" opacity="0.8"/>
        <ellipse cx="86" cy="90" rx="7" ry="5" fill="#bae6fd" opacity="0.8"/>
        <line x1="44" y1="46" x2="36" y2="24" stroke="#0ea5e9" stroke-width="3" stroke-linecap="round"/>
        <circle cx="36" cy="24" r="6" fill="#38bdf8"/>
        <line x1="76" y1="46" x2="84" y2="24" stroke="#0ea5e9" stroke-width="3" stroke-linecap="round"/>
        <circle cx="84" cy="24" r="6" fill="#38bdf8"/>
    </g>

    <!-- stage 3: キングスライム -->
    <g v-else-if="stage === 3">
        <!-- 王冠 -->
        <polygon points="24,28 34,12 44,24 54,8 64,24 74,12 84,28 84,36 24,36" fill="#fbbf24"/>
        <circle cx="34" cy="14" r="4" fill="#ef4444"/>
        <circle cx="54" cy="10" r="5" fill="#3b82f6"/>
        <circle cx="74" cy="14" r="4" fill="#ef4444"/>
        <ellipse cx="60" cy="92" rx="46" ry="42" fill="#0ea5e9"/>
        <ellipse cx="60" cy="108" rx="46" ry="30" fill="#0284c7"/>
        <ellipse cx="42" cy="70" rx="15" ry="10" fill="white" opacity="0.5"/>
        <circle cx="45" cy="84" r="11" fill="white"/>
        <circle cx="75" cy="84" r="11" fill="white"/>
        <circle cx="46" cy="85" r="7" fill="#075985"/>
        <circle cx="76" cy="85" r="7" fill="#075985"/>
        <circle cx="48" cy="83" r="2.5" fill="white"/>
        <circle cx="78" cy="83" r="2.5" fill="white"/>
        <path d="M46 100 Q60 112 74 100" fill="none" stroke="#075985" stroke-width="3" stroke-linecap="round"/>
        <ellipse cx="32" cy="98" rx="8" ry="5" fill="#7dd3fc" opacity="0.8"/>
        <ellipse cx="88" cy="98" rx="8" ry="5" fill="#7dd3fc" opacity="0.8"/>
    </g>

    <!-- stage 4: 神スライム -->
    <g v-else>
        <!-- 光輪 -->
        <ellipse cx="60" cy="22" rx="30" ry="8" fill="none" stroke="#fbbf24" stroke-width="4" opacity="0.8"/>
        <!-- 王冠 -->
        <polygon points="22,34 34,16 46,30 60,12 74,30 86,16 98,34 98,44 22,44" fill="#fbbf24"/>
        <circle cx="34" cy="18" r="5" fill="#ef4444"/>
        <circle cx="60" cy="14" r="6" fill="#a855f7"/>
        <circle cx="86" cy="18" r="5" fill="#ef4444"/>
        <ellipse cx="60" cy="98" rx="48" ry="44" fill="#0284c7"/>
        <ellipse cx="60" cy="116" rx="48" ry="30" fill="#0369a1"/>
        <ellipse cx="40" cy="74" rx="16" ry="11" fill="white" opacity="0.5"/>
        <circle cx="43" cy="88" r="13" fill="white"/>
        <circle cx="77" cy="88" r="13" fill="white"/>
        <circle cx="44" cy="89" r="8" fill="#fbbf24"/>
        <circle cx="78" cy="89" r="8" fill="#fbbf24"/>
        <circle cx="44" cy="89" r="4" fill="#1e3a5f"/>
        <circle cx="78" cy="89" r="4" fill="#1e3a5f"/>
        <circle cx="46" cy="87" r="1.5" fill="white"/>
        <circle cx="80" cy="87" r="1.5" fill="white"/>
        <path d="M44 106 Q60 120 76 106" fill="none" stroke="#1e3a5f" stroke-width="3" stroke-linecap="round"/>
        <ellipse cx="28" cy="104" rx="9" ry="6" fill="#38bdf8" opacity="0.8"/>
        <ellipse cx="92" cy="104" rx="9" ry="6" fill="#38bdf8" opacity="0.8"/>
    </g>
</template>

<script setup>
defineProps({ stage: { type: Number, default: 0 } })
</script>