<template>
	<div class="mt-8 flex flex-1 flex-row gap-5">
		<AccountProfile class="flex-1" />
		<AccountActions class="flex-1" />
	</div>
</template>

<script>
import AccountProfile from '../AccountProfile.vue';
import AccountActions from '../AccountActions.vue';

export default {
	name: 'SaasSetting',
	components: {
		AccountProfile,
		AccountActions
	}
};
</script>
