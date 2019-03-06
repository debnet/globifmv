<template>
    <div class="videoPlayer">
      <video autoplay
             ref="player"
             width="100%"
             height="100%">
        <source :src="video" type="video/mp4"/>
      </video>
    </div>
</template>

<script>
import { mapActions } from 'vuex'
import { EventBus } from '../utils/event-bus.js'
export default {
  data () {
      return {
      }
  },
  props: {
    video: {
      type: String,
      required: true
    },
    timeCode: {
      type: Number,
      default: 0
    }
  },
  methods : {
    ...mapActions({
      setDisplayChoices: 'globiFmv/setDisplayChoices'
    })
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
</style>