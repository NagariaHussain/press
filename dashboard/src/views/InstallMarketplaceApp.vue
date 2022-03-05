<template>
	<div class="px-4 py-4 text-base sm:px-8">Installing app: {{ app }}</div>
</template>
<script>
export default {
	name: 'ImpersonateTeam',
	props: ['app'],
	resources: {
		optionsForQuickInstall() {
			return {
				method: 'press.api.marketplace.options_for_quick_install'
			};
		}
	},
	async mounted() {
		if (this.app) {
			try {
				console.log(this.app);
			} catch (error) {
				this.$router.replace('/sites/new');
			}
		}
	}
};
</script>
