<template>
    <div class="videoPlayer">
      <b-button class="config" v-b-modal.config><icon name="cog" scale="2"/></b-button>
      <video autoplay
             ref="player"
             width="100%"
             height="100%">
        <source :src="video" type="video/mp4"/>
      </video>
      <b-modal id="config"
               title="Configuration"
               ok-only ok-title="Ok"
               ok-variant="outline-dark">
        <p>Qualité</p>
        <b-button variant="outline-dark" @click="setQuality('SD')">SD</b-button>
        <b-button variant="outline-dark" @click="setQuality('HD')">HD</b-button>
        <p>Volume</p>
        <b-form-input type="range"
                      step="0.01"
                      min="0"
                      max="1"
                      v-model="volume"/>
      </b-modal>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import { EventBus } from '../utils/event-bus.js'
import 'vue-awesome/icons/cog'
export default {
  data () {
      return {
      }
  },
  props: {
    video: {
      type: String,
      required: true
    }
  },
  methods : {
    ...mapActions({
      setQuality: 'globiFmv/setQuality'
    })
  },
  computed : {
    volume : {
      get () {
        if(this.$refs.player) {
          return this.$refs.player.volume
        } else {
          return '1'
        }
      },
      set (value) {
        this.$refs.player.volume = value
      }
    }
  },
  created () {
    this.interval = setInterval(() => {
      EventBus.$emit('video-timer', this.$refs.player.currentTime)
    }, 500)
  },
  watch: {
    video : function (value) {
      this.$refs.player.src = value
    }
  },
  destroyed: function () {
    clearInterval(this.interval)
  }
}
</script>

<style>
.videoPlayer{
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