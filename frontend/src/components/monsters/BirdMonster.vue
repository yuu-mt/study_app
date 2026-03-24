<template>
    <!-- stage 0: たまご -->
    <g v-if="stage === 0">
        <defs>
        <radialGradient id="birdEgg" cx="38%" cy="35%">
            <stop offset="0%" stop-color="#fef08a"/>
            <stop offset="100%" stop-color="#fbbf24"/>
        </radialGradient>
        </defs>
        <ellipse cx="60" cy="78" rx="38" ry="48" fill="url(#birdEgg)" stroke="#f59e0b" stroke-width="1.5" style="animation: wobble 2s ease-in-out infinite"/>
        <ellipse cx="46" cy="60" rx="12" ry="8" fill="white" opacity="0.5"/>
        <ellipse cx="72" cy="85" rx="6" ry="4" fill="#fbbf24" opacity="0.2" transform="rotate(-20 72 85)"/>
        <ellipse cx="52" cy="94" rx="5" ry="3" fill="#fbbf24" opacity="0.15" transform="rotate(15 52 94)"/>
    </g>

    <!-- stage 1: ちびチョコボ -->
    <g v-else-if="stage === 1">
        <!-- もさもさ尻尾 -->
        <ellipse cx="94" cy="92" rx="16" ry="11" fill="#fbbf24" transform="rotate(20 94 92)"/>
        <ellipse cx="102" cy="84" rx="13" ry="9" fill="#fde047" transform="rotate(-10 102 84)"/>
        <ellipse cx="97" cy="103" rx="11" ry="8" fill="#f59e0b" transform="rotate(30 97 103)"/>
        <ellipse cx="106" cy="93" rx="9" ry="6" fill="#fbbf24" transform="rotate(-20 106 93)"/>
        <!-- 体 -->
        <ellipse cx="58" cy="96" rx="36" ry="32" fill="#fde047"/>
        <!-- 大きな羽 -->
        <path d="M28 80 Q-8 52 4 28 Q20 38 26 68" fill="#fbbf24" opacity="0.9"/>
        <path d="M28 80 Q-10 56 2 26" fill="none" stroke="#f59e0b" stroke-width="1.5"/>
        <path d="M86 80 Q122 52 110 28 Q94 38 88 68" fill="#fbbf24" opacity="0.9"/>
        <path d="M86 80 Q124 56 112 26" fill="none" stroke="#f59e0b" stroke-width="1.5"/>
        <!-- 頭 -->
        <circle cx="58" cy="60" r="28" fill="#fde047"/>
        <!-- とさか -->
        <path d="M50 34 Q54 18 58 12 Q62 18 66 34" fill="#f59e0b"/>
        <path d="M44 36 Q47 22 52 18" fill="#fbbf24" stroke="#f59e0b" stroke-width="1"/>
        <!-- 目 -->
        <circle cx="48" cy="56" r="9" fill="white"/>
        <circle cx="68" cy="56" r="9" fill="white"/>
        <circle cx="49" cy="57" r="5" fill="#1c1917"/>
        <circle cx="69" cy="57" r="5" fill="#1c1917"/>
        <circle cx="50" cy="55" r="2" fill="white"/>
        <circle cx="70" cy="55" r="2" fill="white"/>
        <!-- くちばし -->
        <ellipse cx="58" cy="70" rx="14" ry="6" fill="#f97316"/>
        <path d="M44 68 Q58 78 72 68" fill="none" stroke="#ea580c" stroke-width="1.5"/>
        <!-- ほっぺ -->
        <ellipse cx="36" cy="62" rx="7" ry="5" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="80" cy="62" rx="7" ry="5" fill="#fca5a5" opacity="0.6"/>
        <!-- 足 -->
        <path d="M48 126 L44 142" stroke="#f59e0b" stroke-width="6" stroke-linecap="round"/>
        <path d="M44,142 L38,148 M44,142 L44,149 M44,142 L50,147" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M68 126 L72 142" stroke="#f59e0b" stroke-width="6" stroke-linecap="round"/>
        <path d="M72,142 L78,148 M72,142 L72,149 M72,142 L66,147" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round"/>
    </g>

    <!-- stage 2: チョコボ -->
    <g v-else-if="stage === 2">
        <!-- もさもさ尻尾（大） -->
        <ellipse cx="100" cy="100" rx="20" ry="14" fill="#fbbf24" transform="rotate(20 100 100)"/>
        <ellipse cx="110" cy="90" rx="17" ry="12" fill="#fde047" transform="rotate(-10 110 90)"/>
        <ellipse cx="104" cy="114" rx="15" ry="10" fill="#f59e0b" transform="rotate(35 104 114)"/>
        <ellipse cx="114" cy="102" rx="13" ry="9" fill="#fbbf24" transform="rotate(-25 114 102)"/>
        <ellipse cx="106" cy="122" rx="11" ry="7" fill="#fde047" transform="rotate(10 106 122)"/>
        <!-- 体 -->
        <ellipse cx="54" cy="106" rx="46" ry="42" fill="#fde047"/>
        <!-- 大きな羽 -->
        <path d="M14 88 Q-30 52 -14 18 Q8 32 12 76" fill="#fbbf24" opacity="0.92"/>
        <path d="M14 88 Q-32 56 -18 16" fill="none" stroke="#f59e0b" stroke-width="2"/>
        <path d="M92 88 Q136 52 120 18 Q98 32 94 76" fill="#fbbf24" opacity="0.92"/>
        <path d="M92 88 Q138 56 124 16" fill="none" stroke="#f59e0b" stroke-width="2"/>
        <!-- 頭 -->
        <ellipse cx="54" cy="58" rx="34" ry="32" fill="#fde047"/>
        <!-- とさか（大） -->
        <path d="M44 30 Q50 8 54 0 Q58 8 64 30" fill="#f59e0b"/>
        <path d="M36 32 Q40 10 48 6" fill="#fbbf24" stroke="#f59e0b" stroke-width="1.5"/>
        <path d="M72 32 Q68 10 60 6" fill="#fbbf24" stroke="#f59e0b" stroke-width="1.5"/>
        <!-- 目 -->
        <circle cx="42" cy="54" r="11" fill="white"/>
        <circle cx="66" cy="54" r="11" fill="white"/>
        <circle cx="43" cy="55" r="6" fill="#1c1917"/>
        <circle cx="67" cy="55" r="6" fill="#1c1917"/>
        <circle cx="44" cy="53" r="2.5" fill="white"/>
        <circle cx="68" cy="53" r="2.5" fill="white"/>
        <!-- くちばし -->
        <ellipse cx="54" cy="72" rx="18" ry="7" fill="#f97316"/>
        <path d="M36 70 Q54 82 72 70" fill="none" stroke="#ea580c" stroke-width="1.5"/>
        <!-- ほっぺ -->
        <ellipse cx="28" cy="62" rx="8" ry="6" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="80" cy="62" rx="8" ry="6" fill="#fca5a5" opacity="0.6"/>
        <!-- 足 -->
        <path d="M38 144 L32 164" stroke="#f59e0b" stroke-width="8" stroke-linecap="round"/>
        <path d="M32,164 L24,172 M32,164 L32,172 M32,164 L40,170" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
        <path d="M70 144 L76 164" stroke="#f59e0b" stroke-width="8" stroke-linecap="round"/>
        <path d="M76,164 L84,172 M76,164 L76,172 M76,164 L68,170" stroke="#f59e0b" stroke-width="3" stroke-linecap="round"/>
    </g>

    <!-- stage 3: 大型チョコボ -->
    <g v-else-if="stage === 3">
        <!-- もさもさ尻尾（豪華） -->
        <ellipse cx="104" cy="104" rx="22" ry="16" fill="#fbbf24" transform="rotate(20 104 104)"/>
        <ellipse cx="116" cy="92" rx="19" ry="14" fill="#fde047" transform="rotate(-15 116 92)"/>
        <ellipse cx="108" cy="120" rx="17" ry="12" fill="#f59e0b" transform="rotate(35 108 120)"/>
        <ellipse cx="120" cy="108" rx="15" ry="11" fill="#fbbf24" transform="rotate(-25 120 108)"/>
        <ellipse cx="110" cy="130" rx="13" ry="9" fill="#fde047"/>
        <ellipse cx="124" cy="118" rx="11" ry="8" fill="#f59e0b"/>
        <!-- 体 -->
        <ellipse cx="52" cy="112" rx="52" ry="48" fill="#fbbf24"/>
        <!-- 超大きな羽 -->
        <path d="M4 92 Q-48 48 -28 6 Q-2 24 4 80" fill="#f59e0b" opacity="0.9"/>
        <path d="M4 92 Q-52 52 -34 4" fill="none" stroke="#d97706" stroke-width="2"/>
        <path d="M16 86 Q-32 46 -14 8" fill="none" stroke="#fde047" stroke-width="1.5" opacity="0.6"/>
        <path d="M100 92 Q152 48 132 6 Q106 24 100 80" fill="#f59e0b" opacity="0.9"/>
        <path d="M100 92 Q156 52 138 4" fill="none" stroke="#d97706" stroke-width="2"/>
        <path d="M88 86 Q136 46 118 8" fill="none" stroke="#fde047" stroke-width="1.5" opacity="0.6"/>
        <!-- 頭 -->
        <ellipse cx="52" cy="58" rx="38" ry="36" fill="#fbbf24"/>
        <!-- とさか（赤く長い） -->
        <path d="M40 26 Q46 -2 52 -12 Q58 -2 64 26" fill="#ef4444"/>
        <path d="M30 28 Q35 0 44 -6" fill="#f97316" stroke="#ef4444" stroke-width="2"/>
        <path d="M74 28 Q69 0 60 -6" fill="#f97316" stroke="#ef4444" stroke-width="2"/>
        <!-- 目 -->
        <circle cx="38" cy="54" r="13" fill="white"/>
        <circle cx="66" cy="54" r="13" fill="white"/>
        <circle cx="39" cy="55" r="7" fill="#1c1917"/>
        <circle cx="67" cy="55" r="7" fill="#1c1917"/>
        <circle cx="40" cy="53" r="3" fill="white"/>
        <circle cx="68" cy="53" r="3" fill="white"/>
        <!-- くちばし -->
        <ellipse cx="52" cy="74" rx="20" ry="9" fill="#f97316"/>
        <path d="M32 72 Q52 86 72 72" fill="none" stroke="#ea580c" stroke-width="2"/>
        <!-- ほっぺ -->
        <ellipse cx="22" cy="64" rx="10" ry="7" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="82" cy="64" rx="10" ry="7" fill="#fca5a5" opacity="0.6"/>
        <!-- 足 -->
        <path d="M32 156 L24 178" stroke="#d97706" stroke-width="9" stroke-linecap="round"/>
        <path d="M24,178 L14,188 M24,178 L24,188 M24,178 L34,186" stroke="#d97706" stroke-width="3.5" stroke-linecap="round"/>
        <path d="M72 156 L80 178" stroke="#d97706" stroke-width="9" stroke-linecap="round"/>
        <path d="M80,178 L90,188 M80,178 L80,188 M80,178 L70,186" stroke="#d97706" stroke-width="3.5" stroke-linecap="round"/>
    </g>

    <!-- stage 4: 伝説のチョコボ -->
    <g v-else>
        <!-- 光輪 -->
        <ellipse cx="52" cy="18" rx="36" ry="9" fill="none" stroke="#fbbf24" stroke-width="4" opacity="0.8"/>
        <!-- もさもさ尻尾（最大） -->
        <ellipse cx="108" cy="108" rx="24" ry="18" fill="#fbbf24" transform="rotate(20 108 108)"/>
        <ellipse cx="122" cy="94" rx="21" ry="16" fill="#fde047" transform="rotate(-15 122 94)"/>
        <ellipse cx="114" cy="126" rx="19" ry="14" fill="#f59e0b" transform="rotate(40 114 126)"/>
        <ellipse cx="128" cy="112" rx="17" ry="13" fill="#fbbf24" transform="rotate(-25 128 112)"/>
        <ellipse cx="118" cy="138" rx="15" ry="11" fill="#fde047"/>
        <ellipse cx="132" cy="124" rx="13" ry="9" fill="#f59e0b"/>
        <ellipse cx="122" cy="148" rx="11" ry="8" fill="#fbbf24"/>
        <!-- 体（金色） -->
        <ellipse cx="50" cy="116" rx="56" ry="52" fill="#fde047"/>
        <!-- 超豪華な翼 -->
        <path d="M-4 96 Q-64 46 -42 -2 Q-10 18 -2 84" fill="#fbbf24" opacity="0.95"/>
        <path d="M-4 96 Q-68 50 -48 -4" fill="none" stroke="#d97706" stroke-width="2.5"/>
        <path d="M12 88 Q-44 42 -26 -2" fill="none" stroke="#fef08a" stroke-width="2" opacity="0.7"/>
        <path d="M104 96 Q164 46 142 -2 Q110 18 102 84" fill="#fbbf24" opacity="0.95"/>
        <path d="M104 96 Q168 50 148 -4" fill="none" stroke="#d97706" stroke-width="2.5"/>
        <path d="M88 88 Q144 42 126 -2" fill="none" stroke="#fef08a" stroke-width="2" opacity="0.7"/>
        <!-- 頭 -->
        <ellipse cx="50" cy="58" rx="42" ry="40" fill="#fde047"/>
        <!-- とさか（王冠風・豪華） -->
        <path d="M36 24 Q42 -8 50 -20 Q58 -8 64 24" fill="#ef4444"/>
        <path d="M24 28 Q30 -4 40 -12" fill="#f97316" stroke="#ef4444" stroke-width="2.5"/>
        <path d="M76 28 Q70 -4 60 -12" fill="#f97316" stroke="#ef4444" stroke-width="2.5"/>
        <!-- 宝石 -->
        <circle cx="50" cy="-18" r="6" fill="#a855f7"/>
        <circle cx="32" cy="-8" r="4" fill="#3b82f6"/>
        <circle cx="68" cy="-8" r="4" fill="#3b82f6"/>
        <!-- 目（金色） -->
        <circle cx="34" cy="54" r="15" fill="white"/>
        <circle cx="66" cy="54" r="15" fill="white"/>
        <circle cx="35" cy="55" r="9" fill="#fbbf24"/>
        <circle cx="67" cy="55" r="9" fill="#fbbf24"/>
        <circle cx="35" cy="55" r="5" fill="#1c1917"/>
        <circle cx="67" cy="55" r="5" fill="#1c1917"/>
        <circle cx="36" cy="53" r="2" fill="white"/>
        <circle cx="68" cy="53" r="2" fill="white"/>
        <!-- くちばし -->
        <ellipse cx="50" cy="76" rx="22" ry="10" fill="#f97316"/>
        <path d="M28 74 Q50 90 72 74" fill="none" stroke="#ea580c" stroke-width="2"/>
        <!-- ほっぺ -->
        <ellipse cx="16" cy="66" rx="11" ry="8" fill="#fca5a5" opacity="0.6"/>
        <ellipse cx="84" cy="66" rx="11" ry="8" fill="#fca5a5" opacity="0.6"/>
        <!-- 足 -->
        <path d="M28 162 L18 186" stroke="#d97706" stroke-width="10" stroke-linecap="round"/>
        <path d="M18,186 L6,198 M18,186 L18,198 M18,186 L30,196" stroke="#d97706" stroke-width="4" stroke-linecap="round"/>
        <path d="M72 162 L82 186" stroke="#d97706" stroke-width="10" stroke-linecap="round"/>
        <path d="M82,186 L94,198 M82,186 L82,198 M82,186 L70,196" stroke="#d97706" stroke-width="4" stroke-linecap="round"/>
    </g>
    </template>

    <script setup>
    defineProps({ stage: { type: Number, default: 0 } })
</script>