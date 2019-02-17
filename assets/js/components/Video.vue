<template>
    <div class="videoPlayer">
      <b-embed autoplay
             width="100%"
             height="100%">
        <source :src="video"/>
      </b-embed>
    </div>
</template>

<script>
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
  }
}
</script>

<style>
.videoPlayer{
  height: 100%;
  background-color: dimgrey;
}
</style>