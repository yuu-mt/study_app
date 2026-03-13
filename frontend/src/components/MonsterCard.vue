<template>
  <div class="monster-card">
    <div class="monster-display">
      <!-- たまご -->
      <svg v-if="monster.stage === 0" viewBox="0 0 120 140" class="monster-svg">
        <defs>
          <radialGradient id="eggGrad" cx="40%" cy="35%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="100%" stop-color="#c7d8f0"/>
          </radialGradient>
        </defs>
        <ellipse cx="60" cy="75" rx="38" ry="48" fill="url(#eggGrad)" stroke="#93c5fd" stroke-width="2" class="egg-body"/>
        <ellipse cx="48" cy="62" rx="6" ry="8" fill="white" opacity="0.6"/>
      </svg>

      <!-- ひよこドラゴン -->
      <svg v-else-if="monster.stage === 1" viewBox="0 0 120 140" class="monster-svg">
        <defs>
          <radialGradient id="babyGrad" cx="40%" cy="35%">
            <stop offset="0%" stop-color="#fde68a"/>
            <stop offset="100%" stop-color="#f59e0b"/>
          </radialGradient>
        </defs>
        <!-- 体 -->
        <ellipse cx="60" cy="90" rx="30" ry="32" fill="url(#babyGrad)" class="float-body"/>
        <!-- 頭 -->
        <circle cx="60" cy="55" r="22" fill="url(#babyGrad)"/>
        <!-- 角 -->
        <polygon points="55,35 60,22 65,35" fill="#ef4444"/>
        <polygon points="63,33 67,21 71,33" fill="#ef4444"/>
        <!-- 目 -->
        <circle cx="52" cy="52" r="5" fill="white"/>
        <circle cx="68" cy="52" r="5" fill="white"/>
        <circle cx="53" cy="53" r="3" fill="#1e293b"/>
        <circle cx="69" cy="53" r="3" fill="#1e293b"/>
        <!-- ほっぺ -->
        <ellipse cx="45" cy="60" rx="5" ry="3" fill="#fca5a5" opacity="0.7"/>
        <ellipse cx="75" cy="60" rx="5" ry="3" fill="#fca5a5" opacity="0.7"/>
        <!-- 口 -->
        <path d="M54 62 Q60 68 66 62" fill="none" stroke="#92400e" stroke-width="1.5" stroke-linecap="round"/>
        <!-- 羽 -->
        <ellipse cx="28" cy="92" rx="12" ry="8" fill="#fcd34d" transform="rotate(-20 28 92)"/>
        <ellipse cx="92" cy="92" rx="12" ry="8" fill="#fcd34d" transform="rotate(20 92 92)"/>
        <!-- 足 -->
        <ellipse cx="50" cy="120" rx="8" ry="5" fill="#f59e0b"/>
        <ellipse cx="70" cy="120" rx="8" ry="5" fill="#f59e0b"/>
      </svg>

      <!-- こドラゴン -->
    <svg v-else-if="monster.stage === 2" viewBox="0 0 120 150" class="monster-svg">
    <defs>
        <radialGradient id="youngGrad" cx="40%" cy="35%">
        <stop offset="0%" stop-color="#4ade80"/>
        <stop offset="100%" stop-color="#15803d"/>
        </radialGradient>
    </defs>
    <!-- 尻尾 -->
    <path d="M88 115 Q118 98 112 72 Q106 52 94 64" fill="none" stroke="#15803d" stroke-width="9" stroke-linecap="round"/>
    <!-- 尻尾の棘 -->
    <polygon points="94,64 106,52 100,68" fill="#86efac"/>
    <polygon points="104,78 116,68 108,82" fill="#86efac"/>
    <!-- 体 -->
    <ellipse cx="58" cy="100" rx="30" ry="33" fill="url(#youngGrad)" class="float-body"/>
    <!-- 腹 -->
    <ellipse cx="58" cy="104" rx="18" ry="22" fill="#86efac" opacity="0.5"/>
    <!-- 背中の棘 -->
    <polygon points="42,78 36,60 48,74" fill="#86efac"/>
    <polygon points="55,70 52,50 62,68" fill="#86efac"/>
    <polygon points="68,72 68,52 76,70" fill="#86efac"/>
    <!-- 翼 -->
    <path d="M30 88 Q8 58 22 44 Q36 50 40 78" fill="#16a34a" opacity="0.85"/>
    <path d="M10 48 Q20 40 28 52" fill="none" stroke="#4ade80" stroke-width="1.5"/>
    <path d="M86 88 Q108 58 94 44 Q80 50 76 78" fill="#16a34a" opacity="0.85"/>
    <path d="M106 48 Q96 40 88 52" fill="none" stroke="#4ade80" stroke-width="1.5"/>
    <!-- 頭 -->
    <path d="M34 62 Q38 36 58 30 Q78 36 82 62 Q78 82 58 84 Q38 82 34 62Z" fill="url(#youngGrad)"/>
    <!-- 角（鋭い） -->
    <polygon points="46,38 42,18 52,36" fill="#dc2626"/>
    <polygon points="58,34 56,12 64,34" fill="#dc2626"/>
    <polygon points="70,38 74,18 64,36" fill="#dc2626"/>
    <!-- 眉毛（鋭く） -->
    <path d="M44 52 L54 48" stroke="#15803d" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M62 48 L72 52" stroke="#15803d" stroke-width="2.5" stroke-linecap="round"/>
    <!-- 目（縦長） -->
    <ellipse cx="50" cy="56" rx="6" ry="7" fill="#fef9c3"/>
    <ellipse cx="66" cy="56" rx="6" ry="7" fill="#fef9c3"/>
    <ellipse cx="50" cy="57" rx="3" ry="5" fill="#15803d"/>
    <ellipse cx="66" cy="57" rx="3" ry="5" fill="#15803d"/>
    <ellipse cx="50" cy="57" rx="1.5" ry="3" fill="#052e16"/>
    <ellipse cx="66" cy="57" rx="1.5" ry="3" fill="#052e16"/>
    <!-- 鼻孔 -->
    <ellipse cx="55" cy="68" rx="2.5" ry="1.5" fill="#14532d"/>
    <ellipse cx="61" cy="68" rx="2.5" ry="1.5" fill="#14532d"/>
    <!-- 口・牙 -->
    <path d="M46 74 Q58 82 70 74" fill="none" stroke="#14532d" stroke-width="2" stroke-linecap="round"/>
    <polygon points="52,75 49,84 55,82" fill="white"/>
    <polygon points="64,75 67,84 61,82" fill="white"/>
    <!-- 爪付き足 -->
    <path d="M44 128 L38 144" stroke="#15803d" stroke-width="6" stroke-linecap="round"/>
    <path d="M38,144 L34,150 M38,144 L38,151 M38,144 L42,150" stroke="#15803d" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M54 132 L50 148" stroke="#15803d" stroke-width="6" stroke-linecap="round"/>
    <path d="M50,148 L46,154 M50,148 L50,155 M50,148 L54,154" stroke="#15803d" stroke-width="2.5" stroke-linecap="round"/>
    <path d="M70 132 L74 148" stroke="#15803d" stroke-width="6" stroke-linecap="round"/>
    <path d="M74,148 L70,154 M74,148 L74,155 M74,148 L78,154" stroke="#15803d" stroke-width="2.5" stroke-linecap="round"/>
</svg>

      <!-- ドラゴン -->
      <svg v-else-if="monster.stage === 3" viewBox="0 0 140 160" class="monster-svg">
        <defs>
          <radialGradient id="dragonGrad" cx="40%" cy="35%">
            <stop offset="0%" stop-color="#818cf8"/>
            <stop offset="100%" stop-color="#4338ca"/>
          </radialGradient>
          <radialGradient id="fireGrad" cx="50%" cy="0%">
            <stop offset="0%" stop-color="#fef08a"/>
            <stop offset="50%" stop-color="#f97316"/>
            <stop offset="100%" stop-color="#dc2626" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <!-- 炎 -->
        <ellipse cx="70" cy="18" rx="8" ry="14" fill="url(#fireGrad)" class="fire"/>
        <!-- 尻尾 -->
        <path d="M100 125 Q130 110 125 85 Q120 65 108 78" fill="none" stroke="#4338ca" stroke-width="10" stroke-linecap="round"/>
        <polygon points="108,78 118,68 112,82" fill="#6366f1"/>
        <!-- 体 -->
        <ellipse cx="68" cy="108" rx="36" ry="38" fill="url(#dragonGrad)" class="float-body"/>
        <!-- 腹 -->
        <ellipse cx="68" cy="112" rx="22" ry="26" fill="#a5b4fc" opacity="0.5"/>
        <!-- 翼 -->
        <path d="M34 90 Q5 55 22 38 Q38 45 42 78" fill="#6366f1" opacity="0.9"/>
        <path d="M7 42 Q18 35 25 45" fill="none" stroke="#818cf8" stroke-width="2"/>
        <path d="M102 90 Q135 55 118 38 Q102 45 98 78" fill="#6366f1" opacity="0.9"/>
        <path d="M133 42 Q122 35 115 45" fill="none" stroke="#818cf8" stroke-width="2"/>
        <!-- 頭 -->
        <ellipse cx="68" cy="62" rx="26" ry="24" fill="url(#dragonGrad)"/>
        <!-- 角 -->
        <polygon points="56,40 60,22 65,40" fill="#dc2626"/>
        <polygon points="65,38 69,18 73,38" fill="#dc2626"/>
        <polygon points="73,40 77,24 81,40" fill="#dc2626"/>
        <!-- 目 -->
        <circle cx="58" cy="58" r="7" fill="white"/>
        <circle cx="78" cy="58" r="7" fill="white"/>
        <circle cx="59" cy="59" r="4" fill="#1e1b4b"/>
        <circle cx="79" cy="59" r="4" fill="#1e1b4b"/>
        <circle cx="60" cy="57" r="1.5" fill="white"/>
        <circle cx="80" cy="57" r="1.5" fill="white"/>
        <!-- 鼻 -->
        <ellipse cx="65" cy="70" rx="3" ry="2" fill="#3730a3"/>
        <ellipse cx="71" cy="70" rx="3" ry="2" fill="#3730a3"/>
        <!-- 口・牙 -->
        <path d="M56 76 Q68 85 80 76" fill="none" stroke="#3730a3" stroke-width="2" stroke-linecap="round"/>
        <polygon points="62,78 60,86 64,84" fill="white"/>
        <polygon points="74,78 76,86 72,84" fill="white"/>
        <!-- 足 -->
        <path d="M50 140 L44 155 M58 144 L55 158" stroke="#4338ca" stroke-width="6" stroke-linecap="round"/>
        <path d="M86 140 L92 155 M78 144 L81 158" stroke="#4338ca" stroke-width="6" stroke-linecap="round"/>
      </svg>

      <!-- 伝説のドラゴン -->
      <svg v-else viewBox="0 0 140 160" class="monster-svg legend">
        <defs>
          <radialGradient id="legendGrad" cx="40%" cy="35%">
            <stop offset="0%" stop-color="#fde68a"/>
            <stop offset="50%" stop-color="#f59e0b"/>
            <stop offset="100%" stop-color="#b45309"/>
          </radialGradient>
          <radialGradient id="fireGrad2" cx="50%" cy="0%">
            <stop offset="0%" stop-color="#ffffff"/>
            <stop offset="30%" stop-color="#fef08a"/>
            <stop offset="70%" stop-color="#f97316"/>
            <stop offset="100%" stop-color="#dc2626" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <!-- 炎（大） -->
        <ellipse cx="70" cy="14" rx="10" ry="18" fill="url(#fireGrad2)" class="fire"/>
        <ellipse cx="55" cy="20" rx="6" ry="10" fill="url(#fireGrad2)" class="fire" style="animation-delay: 0.3s"/>
        <ellipse cx="85" cy="20" rx="6" ry="10" fill="url(#fireGrad2)" class="fire" style="animation-delay: 0.6s"/>
        <!-- 尻尾 -->
        <path d="M100 125 Q135 108 130 80 Q125 58 110 72" fill="none" stroke="#b45309" stroke-width="12" stroke-linecap="round"/>
        <polygon points="110,72 122,60 114,76" fill="#f59e0b"/>
        <!-- 体 -->
        <ellipse cx="68" cy="108" rx="38" ry="40" fill="url(#legendGrad)" class="float-body"/>
        <!-- 腹（金色） -->
        <ellipse cx="68" cy="112" rx="24" ry="28" fill="#fef3c7" opacity="0.6"/>
        <!-- 翼 -->
        <path d="M32 88 Q0 48 20 30 Q38 38 40 76" fill="#f59e0b" opacity="0.95"/>
        <path d="M3 34 Q16 26 24 38" fill="none" stroke="#fde68a" stroke-width="2.5"/>
        <path d="M104 88 Q140 48 120 30 Q102 38 100 76" fill="#f59e0b" opacity="0.95"/>
        <path d="M137 34 Q124 26 116 38" fill="none" stroke="#fde68a" stroke-width="2.5"/>
        <!-- 頭 -->
        <ellipse cx="68" cy="60" rx="28" ry="26" fill="url(#legendGrad)"/>
        <!-- 王冠 -->
        <rect x="50" y="28" width="36" height="10" rx="2" fill="#f59e0b"/>
        <polygon points="50,28 55,18 60,28" fill="#f59e0b"/>
        <polygon points="63,28 68,16 73,28" fill="#f59e0b"/>
        <polygon points="76,28 81,18 86,28" fill="#f59e0b"/>
        <circle cx="55" cy="26" r="2" fill="#dc2626"/>
        <circle cx="68" cy="24" r="2.5" fill="#dc2626"/>
        <circle cx="81" cy="26" r="2" fill="#dc2626"/>
        <!-- 角 -->
        <polygon points="54,36 57,20 62,36" fill="#dc2626"/>
        <polygon points="74,36 77,20 82,36" fill="#dc2626"/>
        <!-- 目（輝く） -->
        <circle cx="57" cy="57" r="8" fill="white"/>
        <circle cx="79" cy="57" r="8" fill="white"/>
        <circle cx="58" cy="58" r="5" fill="#f59e0b"/>
        <circle cx="80" cy="58" r="5" fill="#f59e0b"/>
        <circle cx="58" cy="58" r="2.5" fill="#1e1b4b"/>
        <circle cx="80" cy="58" r="2.5" fill="#1e1b4b"/>
        <circle cx="59" cy="56" r="1.5" fill="white"/>
        <circle cx="81" cy="56" r="1.5" fill="white"/>
        <!-- 鼻 -->
        <ellipse cx="64" cy="68" rx="3" ry="2" fill="#92400e"/>
        <ellipse cx="72" cy="68" rx="3" ry="2" fill="#92400e"/>
        <!-- 口・牙 -->
        <path d="M54 75 Q68 86 82 75" fill="none" stroke="#92400e" stroke-width="2" stroke-linecap="round"/>
        <polygon points="61,77 58,87 63,85" fill="white"/>
        <polygon points="75,77 78,87 73,85" fill="white"/>
        <!-- 足 -->
        <path d="M48 142 L42 157 M56 146 L53 160" stroke="#b45309" stroke-width="7" stroke-linecap="round"/>
        <path d="M88 142 L94 157 M80 146 L83 160" stroke="#b45309" stroke-width="7" stroke-linecap="round"/>
      </svg>
    </div>

    <div class="monster-info">
      <div class="monster-name">{{ monster.name }}</div>
      <div class="monster-hours">累計 {{ totalHours }}時間</div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressWidth + '%' }"></div>
      </div>
      <div class="next-level" v-if="monster.next">
        次の進化まであと {{ hoursToNext }}時間
      </div>
      <div class="next-level max" v-else>
        🎉 最強のドラゴンに進化した！
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  totalMinutes: {
    type: Number,
    default: 0
  }
})

const stages = [
  { stage: 0, name: 'たまご',           min: 0,    max: 600,   next: 'ひよこドラゴン' },
  { stage: 1, name: 'ひよこドラゴン',   min: 600,  max: 1800,  next: 'こドラゴン' },
  { stage: 2, name: 'こドラゴン',       min: 1800, max: 3600,  next: 'ドラゴン' },
  { stage: 3, name: 'ドラゴン',         min: 3600, max: 6000,  next: '伝説のドラゴン' },
  { stage: 4, name: '伝説のドラゴン',   min: 6000, max: null,  next: null },
]

const totalHours = computed(() => Math.floor(props.totalMinutes / 60))

const monster = computed(() => {
  for (let i = stages.length - 1; i >= 0; i--) {
    if (props.totalMinutes >= stages[i].min) return stages[i]
  }
  return stages[0]
})

const progressWidth = computed(() => {
  if (!monster.value.max) return 100
  const range = monster.value.max - monster.value.min
  const current = props.totalMinutes - monster.value.min
  return Math.min(Math.round((current / range) * 100), 100)
})

const hoursToNext = computed(() => {
  if (!monster.value.max) return 0
  return Math.ceil((monster.value.max - props.totalMinutes) / 60)
})
</script>

<style scoped>
.monster-card {
  background: white;
  border-radius: 12px;
  padding: 16px;
  margin: 16px 16px 0;
  border: 1px solid #e2eaff;
  box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  display: flex;
  align-items: center;
  gap: 16px;
}

.monster-display {
  flex-shrink: 0;
  width: 100px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.monster-svg {
  width: 100px;
  height: 120px;
  animation: float 3s ease-in-out infinite;
}

.monster-svg.legend {
  animation: float 3s ease-in-out infinite, glow 2s ease-in-out infinite;
}

.egg-body {
  animation: wobble 2s ease-in-out infinite;
}

.float-body {
  animation: breathe 3s ease-in-out infinite;
}

.fire {
  animation: flicker 0.8s ease-in-out infinite alternate;
  transform-origin: center bottom;
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

@keyframes wobble {
  0%, 100% { transform: scaleX(1) scaleY(1); }
  25% { transform: scaleX(1.04) scaleY(0.97); }
  75% { transform: scaleX(0.97) scaleY(1.04); }
}

@keyframes breathe {
  0%, 100% { transform: scaleX(1) scaleY(1); }
  50% { transform: scaleX(1.03) scaleY(0.98); }
}

@keyframes flicker {
  0% { transform: scaleX(0.9) scaleY(1.1) translateY(2px); opacity: 0.9; }
  100% { transform: scaleX(1.1) scaleY(0.9) translateY(-2px); opacity: 1; }
}

@keyframes glow {
  0%, 100% { filter: drop-shadow(0 0 4px rgba(245, 158, 11, 0.4)); }
  50% { filter: drop-shadow(0 0 12px rgba(245, 158, 11, 0.8)); }
}

.monster-info {
  flex: 1;
  min-width: 0;
}

.monster-name {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 2px;
}

.monster-hours {
  font-size: 12px;
  color: #64748b;
  margin-bottom: 8px;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 6px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #60a5fa);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.next-level {
  font-size: 11px;
  color: #64748b;
}

.next-level.max {
  color: #f59e0b;
  font-weight: 700;
}
</style>