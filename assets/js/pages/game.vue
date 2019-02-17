<template>
	<div>
		<div class="video">
      <b-button :to="{ name: 'home' }" class="home"><icon name="arrow-circle-left" scale="2" class="home-icone"/></b-button>
      <videoPlayer :video="urlVideo"/>
      <div id="choices">
        Toto
      </div>
		</div>
    <div class="inventory">
    </div>
	</div>
</template>

<script>
import videoPlayer from '../components/Video.vue'
import 'vue-awesome/icons/arrow-circle-left'
import { getScene, getChoices } from '../utils/requests'
export default {
	data () {
		return {
      scene: {},
      choices: []
		}
  },
  computed: {
    quality () {
      return this.$route.params.quality
    },
    urlVideo () {
      if(this.scene && (this.scene.url_high || this.scene.url_low) && (this.quality === 'HD' || this.quality === 'SD')){
        if(this.quality === 'HD'){
          return this.scene.url_high
        } else if (this.quality === 'SD') {
          return this.scene.url_low
        }
      } else {
        return ''
      }
    },
    sceneId () {
      return this.$route.params.sceneId
    }
  },
	methods: {
    getDataScene: async function() {
      let dataScene
      try {
        dataScene = await getScene(this.sceneId)
        this.scene = dataScene.data
      } finally {

      }
    },
    getDataChoices: async function () {
      let dataChoices
      try {
        dataChoices = await getChoices(this.sceneId)
        this.choices = dataChoices.data
      } finally {

      }
    }
	},
	components: {
    videoPlayer
	},
	created: async function () {
    this.getDataScene()
    this.getDataChoices()
	}
}
</script>
<style>
.video {
  height: 80vh;
  position: relative;
}
.inventory {
  height: 20vh;
  background-color: black;
}
#choices {
  position: absolute;
  bottom: 0px;
  height: 15vh;
}
.home {
  position: absolute;
  background: transparent;
  border: none;
  z-index: 10;
}
</style>