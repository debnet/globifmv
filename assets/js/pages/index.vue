<template>
    <div>
        <div class="parallax"></div>
        <div class="content">
            <b-card-group deck>
                <b-card v-for="scenario in scenarios"
                        :key="scenario.id"
                        :title="scenario.name"
                        :img-src="scenario.image"
                        img-alt="Image"
                        img-top
                        tag="article"
                        style="max-width: 30%">
                    <b-card-text>
                        {{scenario.description}}
                    </b-card-text>
                    <b-button slot="footer" @click="onClickOpenScenario(scenario.id, scenario.intro_scene.id)"
                              variant="outline-dark">Commencer le scénario
                    </b-button>
                </b-card>
            </b-card-group>
        </div>
        <b-modal id="modal-center"
                 v-model="modalShow"
                 centered title="Choix de la qualité"
                 ok-only ok-title="Annuler"
                 ok-variant="outline-dark"
                 size="sm">
            <b-button variant="outline-dark" @click="goTo('SD', selectedScenar, selectedScene)">SD</b-button>
            <b-button variant="outline-dark" @click="goTo('HD', selectedScenar, selectedScene)">HD</b-button>
        </b-modal>
    </div>
</template>

<script>
    import {getScenarios, getNextPageScenarios} from '../utils/requests'
    import {mapActions} from 'vuex'

    export default {
        data() {
            return {
                scenarios: [],
                modalShow: false,
                selectedScenar: 0,
                selectedScene: 0
            }
        },
        methods: {
            ...mapActions({
                setQuality: 'globifmv/setQuality',
                setScenario: 'globifmv/setScenario',
                setScene: 'globifmv/setScene',
                startScenario: 'globifmv/startScenario'
            }),
            onClickOpenScenario(scenarioId, sceneId) {
                this.modalShow = true;
                this.selectedScenar = scenarioId;
                this.selectedScene = sceneId
            },
            goTo: async function (quality, scenario, scene) {
                this.setQuality(quality);
                this.setScenario(scenario);
                this.setScene(scene);
                var data = await this.startScenario();
                this.$router.push({name: 'scenar'})
            }
        },
        components: {},
        created: async function () {
            let data;
            try {
                data = await getScenarios;
                this.scenarios = data.data.results;

                // Do more tests du to a lack of scenarii
                if (data.data.pages > 1) {
                    for (var i = 2; i <= data.data.pages; i++) {
                        var newData = await getNextPageScenarios(i);
                        this.scenarios.concat(newData.data.results)
                    }
                }
            } finally {

            }
        }
    }
</script>
<style>
    .parallax {
        background-image: url("~_STATIC_/img/header.jpg");

        height: 300px;

        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;

        margin-bottom: 5px;
    }

    .content {
        padding: 5px;
    }

    body {
        background-color: black;
    }
</style>
