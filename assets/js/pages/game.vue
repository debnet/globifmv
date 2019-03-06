<template>
	<div>
		<div class="video">
      <b-button :to="{ name: 'home' }" class="home"><icon name="arrow-circle-left" scale="2" class="home-icone"/></b-button>
      <videoPlayer :video="urlVideo"
                   :timeCode="scene.timecode"/>
      <div id="choices"
           v-if="displayChoices">
        <b-button variant="light"
                  v-for="choice in choices"
                  :key="choice.id"
                  @click="gotTo(choice.id)">
          {{choice.name}}
        </b-button>
      </div>
		</div>
    <div class="inventory">
    </div>
	</div>
</template>

<script>
import videoPlayer from '../components/Video.vue'
import 'vue-awesome/icons/arrow-circle-left'
import { getScene, getChoices, setChoice } from '../utils/requests'
import { mapGetters, mapActions } from 'vuex'
export default {
	data () {
		return {
      scene: {},
      choices: [],
      interval: null
		}
  },
  computed: {
    ...mapGetters({
      quality: 'globiFmv/quality',
      sceneId: 'globiFmv/scene',
      save: 'globiFmv/save',
      displayChoices: 'globiFmv/displayChoices',
    }),
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
    }
  },
	methods: {
    ...mapActions({
      setScene: 'globiFmv/setScene'
    }),
    getDataScene: async function() {
      let dataScene
      try {
        dataScene = await getScene(this.sceneId)
        this.$set(this, 'scene', dataScene.data)
      } finally {

      }
    },
    getDataChoices: async function () {
      let dataChoices
      try {
        dataChoices = await getChoices(this.sceneId, this.save)
        this.choices = dataChoices.data
      } finally {

      }
    },
    gotTo: async function (choiceId) {
      const dataScene = await setChoice (choiceId, this.save)
      this.setScene(dataScene.data.id)
      this.$set(this, 'scene', dataScene.data)
      this.getDataChoices()
      this.displayChoices = false
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
  width: 100%;
  display: grid;
}
.home {
  position: absolute;
  background: transparent;
  border: none;
  z-index: 10;
}
</style>