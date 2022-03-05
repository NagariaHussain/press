<template>
	<div class="px-4 py-4 text-base sm:px-8">
		<Button v-if="false" :loading="true">Loading</Button>
		<div v-else>
			<h1 class="text-xl">Install {{ app }}</h1>

			<div class="mt-2 grid grid-cols-1 gap-2 md:grid-cols-2">
				<Card title="Sites" subtitle="Select a site to install">
					<div>
						<a
							v-for="site in options.sites"
							class="block rounded-md py-2 px-1 text-base hover:bg-gray-50"
							href="#"
							>{{ site }}</a
						>
					</div>
				</Card>

				<Card title="Private Benches" subtitle="Select a bench to install">
					<div>
						<a
							v-for="bench in options.release_groups"
							class="block rounded-md py-2 px-1 text-base hover:bg-gray-50"
							href="#"
							>{{ bench.title }}</a
						>
					</div>
				</Card>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'InstallMarketplaceApp',
	props: ['app'],
	data() {
		return {
			// Test data
			options: {
				release_groups: [
					{
						name: 'bench-0017',
						title: 'Version 13',
						version: 'Version 13',
						available_app_source: 'SRC-darkify-001'
					},
					{
						name: 'bench-0017',
						title: 'Version 12 Staging',
						version: 'Version 13',
						available_app_source: 'SRC-darkify-001'
					}
				],
				sites: ['lonavala.frappe.cloud', 'hero.frappe.cloud']
			}
		};
	},
	resources: {
		optionsForQuickInstall() {
			return {
				method: 'press.api.marketplace.options_for_quick_install',
				params: {
					marketplace_app: this.app
				},
				auto: true,
				onSuccess(d) {
					console.log(d);
				}
			};
		}
	},
	methods: {
		installAppOnBench(bench) {
			// name: rg name
			// press.api.bench.add_app(name, source, app)
		},

		installAppOnSite(site) {
			// name: site name
			// press.api.site.install_app(name, app, plan=None)
		}
	},
	computed: {
		options() {
			return;
		}
	}
};
</script>
