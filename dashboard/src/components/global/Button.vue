<template>
	<router-link
		v-if="route"
		v-slot="{ href, navigate }"
		:to="route"
		:disabled="isDisabled"
		custom
	>
		<a :href="href" @click="navigate" :class="buttonClasses" v-bind="$attrs">
			<FeatherIcon v-if="iconLeft" :name="iconLeft" class="mr-1.5 h-4 w-4" />
			<template v-if="loading && loadingText">
				{{ loadingText }}
			</template>
			<template v-else-if="icon">
				<FeatherIcon :name="icon" class="h-4 w-4" />
			</template>
			<template v-else>
				<slot></slot>
			</template>
			<FeatherIcon v-if="iconRight" :name="iconRight" class="ml-2 h-4 w-4" />
		</a>
	</router-link>

	<button
		v-else
		:class="buttonClasses"
		@click="handleClick"
		v-bind="$attrs"
		:disabled="isDisabled"
	>
		<LoadingIndicator
			v-if="loading"
			:class="{
				'text-white': type == 'primary',
				'text-gray-600': type == 'secondary',
				'text-red-200': type == 'danger'
			}"
		/>
		<FeatherIcon v-else-if="iconLeft" :name="iconLeft" class="mr-1.5 h-4 w-4" />
		<template v-if="loading && loadingText">
			{{ loadingText }}
		</template>
		<template v-else-if="icon">
			<FeatherIcon :name="icon" class="h-4 w-4" />
		</template>
		<template v-else>
			<slot></slot>
		</template>
		<FeatherIcon v-if="iconRight" :name="iconRight" class="ml-2 h-4 w-4" />
	</button>
</template>
<script>
import FeatherIcon from './FeatherIcon.vue';

export default {
	name: 'Button',
	components: {
		FeatherIcon
	},
	props: {
		type: {
			type: String,
			default: 'secondary'
		},
		disabled: {
			type: Boolean,
			default: false
		},
		iconLeft: {
			type: String,
			default: null
		},
		iconRight: {
			type: String,
			default: null
		},
		icon: {
			type: String,
			default: null
		},
		loading: {
			type: Boolean,
			default: false
		},
		loadingText: {
			type: String,
			default: null
		},
		route: {},
		link: {
			type: String,
			default: null
		},
		size: {
			type: String,
			default: null
		}
	},
	computed: {
		buttonClasses() {
			return [
				'inline-flex items-center justify-center leading-5 rounded-md focus:outline-none',
				this.size == 'small' ? 'text-sm' : 'text-base',
				this.icon ? 'p-1.5' : 'px-3 py-1',
				{
					'opacity-50 cursor-not-allowed pointer-events-none': this.isDisabled,
					'bg-gradient-blue hover:bg-gradient-none hover:bg-blue-500 text-white focus:shadow-outline-blue':
						this.type === 'primary',
					'bg-gray-100 hover:bg-gray-200 text-gray-900 focus:shadow-outline-gray':
						this.type === 'secondary',
					'bg-red-500 hover:bg-red-400 text-white focus:shadow-outline-red':
						this.type === 'danger',
					'bg-white text-gray-900 shadow focus:ring focus:ring-gray-400':
						this.type === 'white'
				}
			];
		},
		isDisabled() {
			return this.disabled || this.loading;
		}
	},
	methods: {
		handleClick() {
			this.route && this.$router.push(this.route);
			this.link ? window.open(this.link, '_blank') : null;
		}
	}
};
</script>
