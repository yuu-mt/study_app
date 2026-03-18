<template>
    <!-- stage 0: たまご -->
    <g v-if="stage === 0">
        <defs>
        <radialGradient id="dinoEgg" cx="38%" cy="35%">
            <stop offset="0%" stop-color="#bbf7d0"/>
            <stop offset="100%" stop-color="#4ade80"/>
        </radialGradient>
        </defs>
        <ellipse cx="60" cy="78" rx="38" ry="48" fill="url(#dinoEgg)" stroke="#86efac" stroke-width="1.5" style="animation: wobble 2s ease-in-out infinite"/>
        <ellipse cx="46" cy="60" rx="12" ry="8" fill="white" opacity="0.5"/>
        <ellipse cx="72" cy="85" rx="6" ry="4" fill="#4ade80" opacity="0.2" transform="rotate(-20 72 85)"/>
        <ellipse cx="52" cy="94" rx="5" ry="3" fill="#4ade80" opacity="0.15" transform="rotate(15 52 94)"/>
    </g>

    <!-- stage 1: ちびブラキオ -->
    <g v-else-if="stage === 1">
        <ellipse cx="60" cy="110" rx="34" ry="28" fill="#4ade80"/>
        <ellipse cx="60" cy="116" rx="22" ry="18" fill="#bbf7d0" opacity="0.6"/>
        <rect x="42" y="132" width="10" height="18" rx="5" fill="#22c55e"/>
        <rect x="56" y="134" width="10" height="17" rx="5" fill="#22c55e"/>
        <rect x="70" y="134" width="10" height="17" rx="5" fill="#22c55e"/>
        <path d="M46 86 Q38 60 44 38 Q50 20 56 16" fill="none" stroke="#4ade80" stroke-width="20" stroke-linecap="round"/>
        <path d="M46 84 Q40 58 46 36 Q52 18 56 14" fill="none" stroke="#86efac" stroke-width="10" stroke-linecap="round" opacity="0.4"/>
        <ellipse cx="58" cy="8" rx="16" ry="13" fill="#4ade80"/>
        <ellipse cx="50" cy="4" rx="6" ry="4" fill="#bbf7d0" opacity="0.5"/>
        <circle cx="52" cy="7" r="5" fill="white"/>
        <circle cx="64" cy="9" r="5" fill="white"/>
        <circle cx="53" cy="8" r="3" fill="#14532d"/>
        <circle cx="65" cy="10" r="3" fill="#14532d"/>
        <circle cx="54" cy="7" r="1" fill="white"/>
        <circle cx="66" cy="9" r="1" fill="white"/>
        <path d="M50 16 Q58 20 66 16" fill="none" stroke="#166534" stroke-width="1.5" stroke-linecap="round"/>
        <ellipse cx="46" cy="6" rx="5" ry="3" fill="#86efac" opacity="0.6"/>
        <circle cx="58" cy="96" r="7" fill="#86efac" opacity="0.5"/>
        <circle cx="68" cy="92" r="6" fill="#86efac" opacity="0.5"/>
    </g>

    <!-- stage 2: ブラキオサウルス -->
    <g v-else-if="stage === 2">
        <ellipse cx="62" cy="118" rx="44" ry="34" fill="#4ade80"/>
        <ellipse cx="62" cy="126" rx="30" ry="22" fill="#bbf7d0" opacity="0.6"/>
        <rect x="36" y="146" width="12" height="22" rx="6" fill="#22c55e"/>
        <rect x="52" y="148" width="12" height="20" rx="6" fill="#22c55e"/>
        <rect x="68" y="148" width="12" height="20" rx="6" fill="#22c55e"/>
        <rect x="84" y="146" width="12" height="22" rx="6" fill="#22c55e"/>
        <path d="M-8 108 Q-14 78 -8 48 Q-2 24 58 118" fill="none" stroke="#4ade80" stroke-width="22" stroke-linecap="round"/>
        <path d="M-6 106 Q-12 76 -6 46 Q0 22 8 8" fill="none" stroke="#86efac" stroke-width="11" stroke-linecap="round" opacity="0.4"/>
        <ellipse cx="10" cy="-2" rx="20" ry="16" fill="#4ade80"/>
        <ellipse cx="2" cy="-6" rx="7" ry="5" fill="#bbf7d0" opacity="0.5"/>
        <circle cx="4" cy="-2" r="6" fill="white"/>
        <circle cx="20" cy="2" r="6" fill="white"/>
        <circle cx="5" cy="-1" r="3.5" fill="#14532d"/>
        <circle cx="21" cy="3" r="3.5" fill="#14532d"/>
        <circle cx="6" cy="-3" r="1.5" fill="white"/>
        <circle cx="22" cy="1" r="1.5" fill="white"/>
        <ellipse cx="24" cy="10" r="3" fill="#166534" transform="rotate(20 24 10)"/>
        <path d="M2 8 Q10 14 20 10" fill="none" stroke="#166534" stroke-width="2" stroke-linecap="round"/>
        <ellipse cx="-4" cy="-4" rx="6" ry="4" fill="#86efac" opacity="0.6"/>
        <circle cx="52" cy="100" r="9" fill="#86efac" opacity="0.5"/>
        <circle cx="66" cy="94" r="8" fill="#86efac" opacity="0.5"/>
        <circle cx="78" cy="100" r="7" fill="#86efac" opacity="0.5"/>
    </g>

    <!-- stage 3: でかブラキオ -->
    <g v-else-if="stage === 3">
        <path d="M98 132 Q118 126 120 106 Q120 88 106 94" fill="none" stroke="#86efac" stroke-width="12" stroke-linecap="round"/>
        <ellipse cx="60" cy="120" rx="50" ry="38" fill="#22c55e"/>
        <ellipse cx="60" cy="130" rx="34" ry="26" fill="#bbf7d0" opacity="0.6"/>
        <rect x="28" y="150" width="14" height="26" rx="7" fill="#16a34a"/>
        <rect x="46" y="152" width="14" height="24" rx="7" fill="#16a34a"/>
        <rect x="66" y="152" width="14" height="24" rx="7" fill="#16a34a"/>
        <rect x="84" y="150" width="14" height="26" rx="7" fill="#16a34a"/>
        <path d="M14 108 Q6 72 14 40 Q20 14 60 120" fill="none" stroke="#22c55e" stroke-width="26" stroke-linecap="round"/>
        <path d="M16 106 Q8 70 16 38 Q22 12 26 2" fill="none" stroke="#86efac" stroke-width="13" stroke-linecap="round" opacity="0.4"/>
        <ellipse cx="28" cy="-8" rx="24" ry="18" fill="#22c55e"/>
        <ellipse cx="18" cy="-12" rx="8" ry="6" fill="#bbf7d0" opacity="0.5"/>
        <circle cx="20" cy="-8" r="7" fill="white"/>
        <circle cx="38" cy="-4" r="7" fill="white"/>
        <circle cx="21" cy="-7" r="4" fill="#14532d"/>
        <circle cx="39" cy="-3" r="4" fill="#14532d"/>
        <circle cx="22" cy="-9" r="1.5" fill="white"/>
        <circle cx="40" cy="-5" r="1.5" fill="white"/>
        <ellipse cx="42" cy="4" r="3.5" fill="#166534" transform="rotate(20 42 4)"/>
        <path d="M18 4 Q28 12 40 6" fill="none" stroke="#166534" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="12" cy="-10" rx="7" ry="5" fill="#86efac" opacity="0.6"/>
        <circle cx="58" cy="98" r="11" fill="#86efac" opacity="0.5"/>
        <circle cx="74" cy="92" r="10" fill="#86efac" opacity="0.5"/>
        <circle cx="88" cy="98" r="9" fill="#86efac" opacity="0.5"/>
    </g>

    <!-- stage 4: 古代ブラキオ -->
    <g v-else>
        <!-- 光のオーラ -->
        <ellipse cx="60" cy="110" rx="58" ry="50" fill="#bbf7d0" opacity="0.15"/>
        <path d="M102 134 Q126 126 128 104 Q128 84 112 90" fill="none" stroke="#86efac" stroke-width="14" stroke-linecap="round"/>
        <polygon points="112,90 126,78 118,94" fill="#bbf7d0"/>
        <ellipse cx="60" cy="122" rx="54" ry="42" fill="#16a34a"/>
        <ellipse cx="60" cy="134" rx="38" ry="28" fill="#dcfce7" opacity="0.6"/>
        <rect x="22" y="156" width="16" height="28" rx="8" fill="#15803d"/>
        <rect x="42" y="158" width="16" height="26" rx="8" fill="#15803d"/>
        <rect x="62" y="158" width="16" height="26" rx="8" fill="#15803d"/>
        <rect x="82" y="156" width="16" height="28" rx="8" fill="#15803d"/>
        <path d="M10 110 Q0 68 10 34 Q18 8 60 122" fill="none" stroke="#16a34a" stroke-width="28" stroke-linecap="round"/>
        <path d="M12 108 Q2 66 12 32 Q20 6 24 -4" fill="none" stroke="#86efac" stroke-width="14" stroke-linecap="round" opacity="0.4"/>
        <!-- 王冠 -->
        <polygon points="12,-18 20,-32 28,-20 36,-36 44,-20 52,-32 60,-18 60,-10 12,-10" fill="#fbbf24"/>
        <circle cx="20" cy="-30" r="4" fill="#ef4444"/>
        <circle cx="36" cy="-34" r="5" fill="#a855f7"/>
        <circle cx="52" cy="-30" r="4" fill="#ef4444"/>
        <ellipse cx="36" cy="-4" rx="26" ry="20" fill="#16a34a"/>
        <ellipse cx="24" cy="-10" rx="9" ry="6" fill="#bbf7d0" opacity="0.5"/>
        <circle cx="26" cy="-4" r="8" fill="white"/>
        <circle cx="46" cy="0" r="8" fill="white"/>
        <circle cx="27" cy="-3" r="5" fill="#fbbf24"/>
        <circle cx="47" cy="1" r="5" fill="#fbbf24"/>
        <circle cx="27" cy="-3" r="2.5" fill="#14532d"/>
        <circle cx="47" cy="1" r="2.5" fill="#14532d"/>
        <circle cx="28" cy="-5" r="1.5" fill="white"/>
        <circle cx="48" cy="-1" r="1.5" fill="white"/>
        <ellipse cx="50" cy="8" r="4" fill="#166534" transform="rotate(20 50 8)"/>
        <path d="M24 8 Q36 16 50 8" fill="none" stroke="#166534" stroke-width="2.5" stroke-linecap="round"/>
        <ellipse cx="14" cy="-8" rx="8" ry="5" fill="#86efac" opacity="0.6"/>
        <circle cx="62" cy="100" r="12" fill="#86efac" opacity="0.5"/>
        <circle cx="78" cy="92" r="11" fill="#86efac" opacity="0.5"/>
        <circle cx="92" cy="100" r="10" fill="#86efac" opacity="0.5"/>
    </g>
</template>

<script setup>
defineProps({ stage: { type: Number, default: 0 } })
</script>