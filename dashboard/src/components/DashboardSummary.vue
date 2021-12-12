<template>
	<div class="w-full flex flex-row items-center justify-between py-5">
		<div
			v-for="card in cards"
			:key="card.title"
			class="pl-6 pr-16 py-4 bg-white border rounded-lg shadow"
		>
			<div class="flex flex-row items-center justify-items-center">
				<div
					:class="[
						'mr-3 rounded-full p-3 flex-shrink-0',
						card.iconBackgroundClass
					]"
				>
					<div class="text-white w-4 h-4">
						<component :is="card.icon" v-if="card.icon" />
					</div>
				</div>
				<div class="flex flex-col">
					<h3 class="text-2xl text-gray-900 font-semibold">{{ card.title }}</h3>
					<p class="text-base text-gray-600">{{ card.subtitle }}</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import CodeEditorIcon from '@/components/icons/CodeEditorIcon.vue';
import UsageIcon from '@/components/icons/UsageIcon.vue';
import AppsIcon from '@/components/icons/AppsIcon.vue';
import InvoiceIcon from '@/components/icons/InvoiceIcon.vue';

export default {
	components: {
		CodeEditorIcon,
		UsageIcon,
		AppsIcon,
		InvoiceIcon
	},
	data() {
		return {
			cards: [
				{
					icon: CodeEditorIcon,
					title: '23 Sites',
					subtitle: 'Under your account',
					link: '#',
					iconBackgroundClass: 'bg-green-500'
				},
				{
					icon: AppsIcon,
					title: '5 Apps',
					subtitle: 'In the Marketplace',
					link: '#',
					iconBackgroundClass: 'bg-yellow-600'
				},
				{
					icon: UsageIcon,
					title: '$4,222.67',
					subtitle: 'Current Usage',
					link: '#',
					iconBackgroundClass: 'bg-teal-600'
				},
				{
					icon: InvoiceIcon,
					title: '3 Invoices',
					subtitle: '$22.50 Outstanding',
					link: '#',
					iconBackgroundClass: 'bg-orange-600'
				}
			]
		};
	}
};
</script>
