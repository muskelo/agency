<template>
	<Header />
	<router-view></router-view>
	<Alerts />
</template>

<script>
import Header from "./components/Header.vue";
import Alerts from "./components/Alerts.vue";
import { useCurrentUserStore } from "./stores/currentUser";
import { useCatalogStore } from "./stores/catalog";

export default {
	data() {
		let currentUser = useCurrentUserStore();
		let catalog = useCatalogStore();
		return {
			currentUser,
			catalog,
		};
	},
	components: {
		Header,
		Alerts,
	},
	methods:{},
	mounted() {
		this.currentUser.init();
		this.catalog.init();
	},
};
</script>

<style lang="scss">
$enable-cssgrid: true;
@import "../node_modules/bootstrap/scss/bootstrap.scss";
</style>


