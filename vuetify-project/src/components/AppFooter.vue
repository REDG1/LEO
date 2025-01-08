<template>
  <v-footer height="40" theme="dark" class="mt-2" app>
    <a
      v-for="item in items"
      :key="item.title"
      :href="item.href"
      :title="item.title"

      class="d-inline-block mx-2 social-link"
      rel="noopener noreferrer"
      target="_blank"
    >
      <v-icon
        :icon="item.icon"
        :size="item.icon === '$mdiMicroscope' ? 28 : 20"
      />
    </a>

    <div
      class="text-caption text-disabled"
      style="position: absolute; right: 16px;"
    >
      &copy; 2024-[[ (new Date()).getFullYear() ]] <span class="d-none d-sm-inline-block">IPHT DataScience </span>
      —
      <a
        class="text-decoration-none on-surface"
        href="https://vuetifyjs.com/about/licensing/"
        rel="noopener noreferrer"
        target="_blank"
      >
        MIT License
      </a>
    </div>
  </v-footer>
</template>

<script setup>

  const items = [
    {
      title: 'Photonic data science group',
      icon: "$mdiMicroscope",
      href: 'https://group.photonicdata.science/',
    },
    {
      title: 'Gitlab',
      icon: "$mdiGitlab",
      href: 'https://git.photonicdata.science/',
    },
    {
      title: 'Github',
      icon: "$mdiGithub",
       href: '#',
    },



  ]

</script>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgba(25, 118, 210, 1)
</style>
