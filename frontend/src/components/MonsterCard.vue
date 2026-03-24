<template>
  <div class="monster-card">
    <div class="monster-display">
      <svg viewBox="0 0 120 170" class="monster-svg">
        <BirdMonster v-if="props.monsterType === 'bird'" :stage="currentStage.stage"/>
        <DragonMonster v-else-if="props.monsterType === 'dragon'" :stage="currentStage.stage"/>
        <DinoMonster v-else-if="props.monsterType === 'dino'" :stage="currentStage.stage"/>
      </svg>
    </div>
    <div class="monster-info">
      <div class="monster-name">{{ currentStage.name }}</div>
      <div class="monster-hours">累計 {{ totalHours }}時間</div>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressWidth + '%', background: progressColor }"></div>
      </div>
      <div class="next-level" v-if="currentStage.next">
        次の進化まであと {{ hoursToNext }}時間
      </div>
      <div class="next-level max" v-else>
        🎉 最強に進化した！
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BirdMonster from './monsters/BirdMonster.vue'
import DragonMonster from './monsters/DragonMonster.vue'
import DinoMonster from './monsters/DinoMonster.vue'

const props = defineProps({
  totalMinutes: { type: Number, default: 0 },
  monsterType: { type: String, default: 'slime' }
})

const totalHours = computed(() => Math.floor(props.totalMinutes / 60))

const stages = {
  bird: [
    { stage: 0, name: '？？？のたまご', min: 0,    max: 600,  next: true,  color: '#fbbf24' },
    { stage: 1, name: 'ちびチョコボ',   min: 600,  max: 1800, next: true,  color: '#fbbf24' },
    { stage: 2, name: 'チョコボ',       min: 1800, max: 3600, next: true,  color: '#f59e0b' },
    { stage: 3, name: '大型チョコボ',   min: 3600, max: 6000, next: true,  color: '#d97706' },
    { stage: 4, name: '伝説のチョコボ', min: 6000, max: null, next: false, color: '#b45309' },
  ],
  dragon: [
    { stage: 0, name: '？？？のたまご', min: 0,    max: 600,  next: true, color: '#f87171' },
    { stage: 1, name: 'ちびドラゴン',     min: 600,  max: 1800, next: true, color: '#f87171' },
    { stage: 2, name: 'こドラゴン',       min: 1800, max: 3600, next: true, color: '#ef4444' },
    { stage: 3, name: 'レッドドラゴン',         min: 3600, max: 6000, next: true, color: '#dc2626' },
    { stage: 4, name: '守護者レッドドラゴン',   min: 6000, max: null, next: false, color: '#b91c1c' },
  ],
  dino: [
    { stage: 0, name: '？？？のたまご',     min: 0,    max: 600,  next: true, color: '#4ade80' },
    { stage: 1, name: 'ちびブラキオ',     min: 600,  max: 1800, next: true, color: '#4ade80' },
    { stage: 2, name: 'ブラキオ', min: 1800, max: 3600, next: true, color: '#22c55e' },
    { stage: 3, name: 'キングブラキオ',     min: 3600, max: 6000, next: true, color: '#16a34a' },
    { stage: 4, name: '古代のブラキオ',     min: 6000, max: null, next: false, color: '#15803d' },
  ],
}

const currentStageData = computed(() => {
  const list = stages[props.monsterType] || stages.slime
  for (let i = list.length - 1; i >= 0; i--) {
    if (props.totalMinutes >= list[i].min) return list[i]
  }
  return list[0]
})

const progressWidth = computed(() => {
  const s = currentStageData.value
  if (!s.max) return 100
  const range = s.max - s.min
  const current = props.totalMinutes - s.min
  return Math.min(Math.round((current / range) * 100), 100)
})

const hoursToNext = computed(() => {
  const s = currentStageData.value
  if (!s.max) return 0
  return Math.ceil((s.max - props.totalMinutes) / 60)
})

const progressColor = computed(() => currentStageData.value.color)

const currentStage = computed(() => {
  const type = props.monsterType
  const stage = currentStageData.value.stage
  return { type, stage, ...currentStageData.value }
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
  height: 130px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.monster-svg {
  width: 100px;
  height: 130px;
  animation: float 3s ease-in-out infinite;
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

@keyframes flicker {
  0% { transform: scaleX(0.9) scaleY(1.1); opacity: 0.9; }
  100% { transform: scaleX(1.1) scaleY(0.9); opacity: 1; }
}

.monster-info {
  flex: 1;
  min-width: 0;
}

.monster-name {
  font-size: 16px;
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
  border-radius: 4px;
  transition: width 0.5s ease;
}

.next-level {
  font-size: 11px;
  color: #64748b;
}

.next-level.max {
  font-weight: 700;
}
</style>