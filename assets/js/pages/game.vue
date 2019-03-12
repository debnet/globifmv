<template>
	<div>
		<div class="video">
      <b-button :to="{ name: 'home' }" class="home"><icon name="arrow-circle-left" scale="2" class="home-icone"/></b-button>
      <videoPlayer :video="urlVideo"
                   :timeCode="scene.timecode"/>
      <div id="choices">
        <div class="d-flex align-items-end justify-content-center">
          <b-button-group vertical class="mx-auto">
            <b-button variant="light"
                    v-for="choice in choicesToDisplay"
                    :key="choice.id"
                    @click="gotTo(choice.id)">
              {{choice.name}}
            </b-button>
          </b-button-group>
        </div>
      </div>
		</div>
    <div class="inventory">
      <div class="d-flex flex-row">
        <div v-if="health" class="p-2 flex-fill life">
          <span>Vie : </span><icon v-for="heart in health" :key="heart" name="heart"/>
        </div>
        <div v-if="money" class="p-2 flex-fill">
          <span>Argent : {{money}}</span>
        </div>
      </div>
    </div>
	</div>
</template>

<script>
import videoPlayer from '../components/Video.vue'
import 'vue-awesome/icons/arrow-circle-left'
import 'vue-awesome/icons/heart'
import { getScene, getChoices, setChoice } from '../utils/requests'
import { mapGetters, mapActions } from 'vuex'
import { EventBus } from '../utils/event-bus.js'
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
      health: 'globiFmv/health',
      money: 'globiFmv/money'
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
    },
    choicesToDisplay () {
      if(this.choices.length > 0 && this.choices.filter(o => o.display).length > 0){
        return this.choices.filter(o => o.display)
      } else {
        return []
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
    },
    verifDisplayChoice (timer) {
      let scope = this
      this.choices.forEach(function (choice) {
        if(choice.timecode <= timer){
          scope.displayChoice(choice.id)
        }
      })
    },
    displayChoice (choiceId) {
      var choice = this.choices.find(o => o.id === choiceId)
      this.$set(choice, 'display', true)
    }
	},
	components: {
    videoPlayer
	},
	created: async function () {
    EventBus.$on('video-timer', this.verifDisplayChoice);
    this.getDataScene()
    this.getDataChoices()
  },
  destroyed: function () {
    EventBus.$off('video-timer', this.verifDisplayChoice)
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
}
.home {
  position: absolute;
  background: transparent;
  border: none;
  z-index: 10;
}

.inventory {
  color: white;
}

.life svg {
  padding-right: 5px; 
}
</style>