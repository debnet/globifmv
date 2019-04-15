<template>
    <div class="videoPlayer">
        <b-button class="config"
                  v-b-modal.config
                  @click="openConfig">
            <icon name="cog" scale="2"/>
        </b-button>
        <video autoplay
               height="100%"
               ref="player"
               width="100%">
            <source :src="video" type="video/mp4"/>
        </video>
        <b-modal id="config"
                 ok-only
                 ok-title="Ok" ok-variant="outline-dark"
                 title="Configuration">
            <p>Qualité</p>
            <b-button @click="setQuality('SD')" variant="outline-dark">SD</b-button>
            <b-button @click="setQuality('HD')" variant="outline-dark">HD</b-button>
            <p>Volume</p>
            <b-form-input max="1"
                          min="0"
                          step="0.01"
                          type="range"
                          v-model="volume"/>
        </b-modal>
    </div>
</template>

<script>
    import {mapActions} from 'vuex'
    import {EventBus} from '../utils/event-bus.js'
    import 'vue-awesome/icons/cog'

    export default {
        data() {
            return {}
        },
        props: {
            video: {
                type: String,
                required: true
            }
        },
        methods: {
            ...mapActions({
                setQuality: 'globifmv/setQuality'
            }),
            openConfig () {
                this.$refs.player.pause()
            }
        },
        computed: {
            volume: {
                get() {
                    if (this.$refs.player) {
                        return this.$refs.player.volume
                    } else {
                        return '1'
                    }
                },
                set(value) {
                    this.$refs.player.volume = value
                }
            }
        },
        created() {
            this.interval = setInterval(() => {
                EventBus.$emit('video-timer', this.$refs.player.currentTime)
            }, 500)
        },
        mounted() {
            this.$root.$on('bv::modal::hide', (bvEvent, modalId) => {
                this.$refs.player.play()
            })
        },
        watch: {
            video: function (value) {
                this.$refs.player.src = value
            }
        },
        destroyed: function () {
            clearInterval(this.interval)
        }
    }
</script>

<style>
    .videoPlayer {
        height: 100%;
        background-color: dimgrey;
    }

    .config {
        position: absolute;
        right: 0;
        background: transparent;
        border: none;
        z-index: 10;
    }
</style>
