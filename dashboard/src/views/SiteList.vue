<template>
	<div
		class="sm:rounded-md sm:border sm:border-gray-100 sm:py-1 sm:px-2 sm:shadow"
	>
		<div class="py-2 text-base text-gray-600 sm:px-2" v-if="sites.length === 0">
			No sites in this bench
		</div>
		<div class="py-2" v-for="(site, index) in sites" :key="site.name">
			<router-link
				:to="`/sites/${site.name}/overview`"
				class="block rounded-md pt-2 hover:bg-gray-50 sm:px-2"
			>
				<div class="flex items-center justify-between sm:justify-start">
					<div class="text-base sm:w-4/12">
						{{ site.name }}
					</div>
					<div class="text-base sm:w-4/12">
						<Badge class="pointer-events-none" v-bind="siteBadge(site)" />
					</div>
					<div class="hidden w-2/12 text-sm text-gray-600 sm:block">
						Created {{ formatDate(site.creation, 'relative') }}
					</div>
					<div class="hidden w-2/12 text-right text-base sm:block">
						<Link
							v-if="site.status === 'Active' || site.status === 'Updating'"
							:to="`https://${site.name}`"
							target="_blank"
							class="inline-flex items-center text-sm"
							@click.stop
						>
							Visit Site
							<FeatherIcon name="external-link" class="ml-1 h-3 w-3" />
						</Link>
					</div>
				</div>
				<div
					class="translate-y-2 transform pt-2"
					:class="{ 'border-b': index < sites.length - 1 }"
				/>
			</router-link>
		</div>
	</div>
</template>
<script>
export default {
	name: 'SiteList',
	props: ['sites'],
	methods: {
		siteBadge(site) {
			let status = site.status;
			let color = null;
			if (site.update_available && site.status == 'Active') {
				status = 'Update Available';
				color = 'blue';
			}

			let usage = Math.max(
				site.current_cpu_usage,
				site.current_database_usage,
				site.current_disk_usage
			);
			if (usage && usage >= 80 && status == 'Active') {
				status = 'Attention Required';
				color = 'yellow';
			}
			if (site.trial_end_date) {
				status = 'Trial';
				color = 'yellow';
			}
			return {
				color,
				status
			};
		}
	}
};
</script>
