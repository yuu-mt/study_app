<template>
    <div class="select-container">
        <div class="header-area">
        <h1>一緒に成長するなかまを選ぼう！</h1>
        <p>好きな卵を選んでください。</p>
        </div>

        <div class="eggs-grid">
            <div
                v-for="monster in monsters"
                :key="monster.id"
                :class="['egg-card', selected === monster.id ? 'selected' : '']"
                @click="selected = monster.id"
            >
                <div class="egg-wrap">
                    <svg viewBox="0 0 100 120" width="100" height="120">
                        <defs>
                        <radialGradient :id="`eggGrad${monster.id}`" cx="38%" cy="35%">
                            <stop offset="0%" :stop-color="monster.eggLight"/>
                            <stop offset="100%" :stop-color="monster.eggDark"/>
                        </radialGradient>
                        </defs>
                        <ellipse cx="50" cy="65" rx="36" ry="46"
                        :fill="`url(#eggGrad${monster.id})`"
                        :stroke="monster.eggDark" stroke-width="1.5"/>
                        <ellipse cx="38" cy="50" rx="12" ry="8" fill="white" opacity="0.5"/>
                        <!-- 卵のもよう -->
                        <ellipse cx="58" cy="72" rx="6" ry="4"
                        :fill="monster.eggDark" opacity="0.2"
                        transform="rotate(-20 58 72)"/>
                        <ellipse cx="44" cy="80" rx="5" ry="3"
                        :fill="monster.eggDark" opacity="0.15"
                        transform="rotate(15 44 80)"/>
                    </svg>
                </div>
                <div v-if="selected === monster.id" class="check">✓</div>
            </div>
        </div>

        <button
            class="btn-start"
            :disabled="!selected"
            @click="startAdventure"
            >
            {{ selected ? 'このなかまと冒険する！' : '卵を選んでください' }}
        </button>
    </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const router = useRouter()
const selected = ref(null)

const monsters = [
    {
        id: 'bird',
        name: '鳥',
        desc: '',
        eggLight: '#fef08a',
        eggDark: '#fbbf24',
    },
    {
        id: 'dragon',
        name: 'ドラゴン',
        desc: 'かっこかわいい！',
        eggLight: '#fecaca',
        eggDark: '#f87171',
    },
    {
        id: 'dino',
        name: 'ブラキオサウルス',
        desc: 'のびのびほのぼの！',
        eggLight: '#bbf7d0',
        eggDark: '#4ade80',
    },
]

const startAdventure = async () => {
    try {
        await api.patch('/accounts/me/', {
        monster_type: selected.value,
        monster_selected: true  // ← これが抜けていた
        })
        localStorage.setItem('monster_type', selected.value)
        router.push('/home')
    } catch (error) {
        console.error(error)
        localStorage.setItem('monster_type', selected.value)
        router.push('/home')
    }
}

</script>

<style scoped>
.select-container {
    max-width: 480px;
    margin: 0 auto;
    padding: 32px 16px;
    min-height: 100vh;
    background: #f8faff;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.header-area {
    text-align: center;
    margin-bottom: 32px;
}

.header-area h1 {
    font-size: 24px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 8px;
}

.header-area p {
    font-size: 14px;
    color: #64748b;
}

.eggs-grid {
    display: flex;
    gap: 16px;
    margin-bottom: 32px;
    flex-wrap: wrap;
    justify-content: center;
}

.egg-card {
    background: white;
    border-radius: 16px;
    padding: 20px 16px;
    border: 2px solid #e2e8f0;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    width: 130px;
}

.egg-card:hover {
    border-color: #93c5fd;
    transform: translateY(-4px);
}

.egg-card.selected {
    border-color: #2563eb;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.1);
}

.egg-wrap {
    display: flex;
    justify-content: center;
    margin-bottom: 10px;
    animation: float 3s ease-in-out infinite;
}

.monster-name {
    font-size: 14px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 4px;
}

.monster-desc {
    font-size: 12px;
    color: #64748b;
}

.check {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 24px;
    height: 24px;
    background: #2563eb;
    color: white;
    border-radius: 50%;
    font-size: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
}

.btn-start {
    width: 100%;
    max-width: 320px;
    padding: 16px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 16px;
    font-weight: 700;
    cursor: pointer;
    transition: opacity 0.2s;
}

.btn-start:disabled {
    background: #94a3b8;
    cursor: not-allowed;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
}
</style>