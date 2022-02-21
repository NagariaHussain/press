<template>
	<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
		<div class="col-span-2">
			<Button class="mb-3 w-16" @click="showShell">Open Database Shell</Button>
			<Card v-if="shellOpen" title="Database Console">
				<iframe
					width="100%"
					scrolling="auto"
					height="335px"
					frameborder="1"
					src="http://localhost:4203"
					style="border: 0px none #ffffff"
					name="national-campaign"
					marginheight="0px"
					marginwidth="0px"
				>
				</iframe>
			</Card>
		</div>
		<SiteDatabaseBackups :site="site" />
		<div><SiteDatabaseRestore :site="site" /></div>
	</div>
</template>

<script>
import SiteDatabaseBackups from './SiteDatabaseBackups.vue';
import SiteDatabaseRestore from './SiteDatabaseRestore.vue';
import Card from '@/components/global/Card.vue';

export default {
	name: 'SiteDatabase',
	props: ['site'],
	data() {
		return {
			shellOpen: false
		};
	},
	components: { SiteDatabaseBackups, SiteDatabaseRestore, Card },
	methods: {
		showShell() {
			this.shellOpen = true;
		}
	}
};
</script>
