<template>
	<div class="mt-8">
		<div class="px-4 sm:px-8" v-if="$account.user">
			<div class="pb-3">
				<div>
					<h1 class="text-3xl font-bold">Settings</h1>
					<div class="mt-2 text-base text-gray-600">
						<span v-if="$account.team.name != $account.user.name">
							Team: {{ $account.team.name }} &middot;
							<!-- prettier-ignore -->
							Member: {{ $account.user.name }}
						</span>
						<span v-else>{{ $account.team.name }}</span>
						<template v-if="$account.team.erpnext_partner">
							&middot;
							<span>ERPNext Partner</span>
						</template>
						&middot;
						<span>
							Member since
							{{
								$date($account.team.creation).toLocaleString({
									month: 'short',
									day: 'numeric',
									year: 'numeric'
								})
							}}
						</span>
					</div>
				</div>
			</div>
		</div>
		<div class="px-4 sm:px-8">
			<Tabs class="pb-32" :tabs="tabs">
				<router-view v-if="$account.user"></router-view>
			</Tabs>
		</div>
	</div>
</template>

<script>
import Tabs from '@/components/Tabs.vue';

export default {
	name: 'Account',
	components: {
		Tabs
	},
	data: () => ({
		tabs: [
			{ label: 'Profile & Team', route: '/account/profile' },
			{ label: 'Billing & Payments', route: '/account/billing' }
		]
	}),
	activated() {
		if (this.$route.matched.length === 1) {
			let path = this.$route.fullPath;
			this.$router.replace(`${path}/profile`);
		}
	},
	beforeRouteUpdate(to, from, next) {
		if (to.path == '/account') {
			next('/account/profile');
		} else {
			next();
		}
	}
};
</script>
