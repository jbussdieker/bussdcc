# Changelog

## [0.16.0](https://github.com/jbussdieker/bussdcc/compare/v0.15.1...v0.16.0) (2026-02-10)


### Features

* **runtime:** introduce ThreadedRuntime and SignalRuntime classes ([a0ba8b2](https://github.com/jbussdieker/bussdcc/commit/a0ba8b2286b804d906120e85369fb76730360c38))

## [0.15.1](https://github.com/jbussdieker/bussdcc/compare/v0.15.0...v0.15.1) (2026-02-10)


### Bug Fixes

* **device, process, runtime:** improve error handling and context management ([c110e11](https://github.com/jbussdieker/bussdcc/commit/c110e111d846bdbc9c608170392b4cefbcf574cc))

## [0.15.0](https://github.com/jbussdieker/bussdcc/compare/v0.14.0...v0.15.0) (2026-02-10)


### Features

* **runtime:** enhance runtime protocol and representation ([c0a510a](https://github.com/jbussdieker/bussdcc/commit/c0a510a4281512cf998ce229b0fa9b81f3f4e52c))


### Bug Fixes

* **runtime:** add property decorator ([eeefe94](https://github.com/jbussdieker/bussdcc/commit/eeefe9421d31d8234d5752566877dedde4c57176))
* **runtime:** ensure idempotent shutdown process ([ce9a1a6](https://github.com/jbussdieker/bussdcc/commit/ce9a1a6ffd8cf44b39bfd32386d3b0c0654a6fdd))

## [0.14.0](https://github.com/jbussdieker/bussdcc/compare/v0.13.0...v0.14.0) (2026-02-09)


### Features

* **runtime:** add lifecycle hooks for boot and shutdown ([13a9958](https://github.com/jbussdieker/bussdcc/commit/13a9958ce5bab2c5e299fc8e35463f56de61247c))

## [0.13.0](https://github.com/jbussdieker/bussdcc/compare/v0.12.0...v0.13.0) (2026-02-09)


### Features

* **event:** enhance event engine with protocol support ([8c9cca9](https://github.com/jbussdieker/bussdcc/commit/8c9cca9e0741cb36d891e5ccdd31c0922055ac64))

## [0.12.0](https://github.com/jbussdieker/bussdcc/compare/v0.11.2...v0.12.0) (2026-02-08)


### Features

* support dependency injection for state and events ([3dc87cb](https://github.com/jbussdieker/bussdcc/commit/3dc87cbea582cf5fddefe819af6731bc2089435c))

## [0.11.2](https://github.com/jbussdieker/bussdcc/compare/v0.11.1...v0.11.2) (2026-02-08)


### Bug Fixes

* add step id ([3cc2814](https://github.com/jbussdieker/bussdcc/commit/3cc2814630a22828e4fe56957e5e54006032d8f4))

## [0.11.1](https://github.com/jbussdieker/bussdcc/compare/v0.11.0...v0.11.1) (2026-02-08)


### Bug Fixes

* add output to release please ([5300644](https://github.com/jbussdieker/bussdcc/commit/5300644f9ff50acb518073d17c70b3adc79b7632))

## [0.11.0](https://github.com/jbussdieker/bussdcc/compare/v0.10.1...v0.11.0) (2026-02-08)


### Features

* publish to pypi ([913657f](https://github.com/jbussdieker/bussdcc/commit/913657f7c45b9a8038f884296725868638b22646))


### Bug Fixes

* expose event and state engine protocol ([ffa14e6](https://github.com/jbussdieker/bussdcc/commit/ffa14e6e4211d345034345f56e00a7fbea4007e9))

## [0.10.1](https://github.com/jbussdieker/bussdcc/compare/v0.10.0...v0.10.1) (2026-02-08)


### Bug Fixes

* add py.typed marker ([d580bd7](https://github.com/jbussdieker/bussdcc/commit/d580bd7c77a7fc1c0563a3be4c4db7a041907d0a))

## [0.10.0](https://github.com/jbussdieker/bussdcc/compare/v0.9.0...v0.10.0) (2026-02-08)


### Features

* make runtime a context handler ([ca11faf](https://github.com/jbussdieker/bussdcc/commit/ca11fafca52a16417862eba820eea69af71356db))

## [0.9.0](https://github.com/jbussdieker/bussdcc/compare/v0.8.0...v0.9.0) (2026-02-07)


### Features

* add device id and rename name to kind ([90cdf31](https://github.com/jbussdieker/bussdcc/commit/90cdf317476c0e2af88a634edacef5f14ea861a9))

## [0.8.0](https://github.com/jbussdieker/bussdcc/compare/v0.7.0...v0.8.0) (2026-02-02)


### Features

* add policy framework ([051700b](https://github.com/jbussdieker/bussdcc/commit/051700b06555bd1c3148edbd95a0cada86772533))


### Documentation

* update readme ([72f2ae7](https://github.com/jbussdieker/bussdcc/commit/72f2ae76701560d6cf39ce10a03502371b0c7b68))

## [0.7.0](https://github.com/jbussdieker/bussdcc/compare/v0.6.1...v0.7.0) (2026-01-31)


### Features

* improve context and runtime boundaries ([f8439ca](https://github.com/jbussdieker/bussdcc/commit/f8439ca71b6cde4612a8f71ba7480c80ec603368))
* use process for interfaces and better boot/shutdown order ([aaffdae](https://github.com/jbussdieker/bussdcc/commit/aaffdae31e8328a775c4edbeeff4dc2bb1f32c75))

## [0.6.1](https://github.com/jbussdieker/bussdcc/compare/v0.6.0...v0.6.1) (2026-01-30)


### Bug Fixes

* remove stray print ([1263c16](https://github.com/jbussdieker/bussdcc/commit/1263c1653ff4b74f74c480f4bab043223d8e4d44))

## [0.6.0](https://github.com/jbussdieker/bussdcc/compare/v0.5.1...v0.6.0) (2026-01-30)


### Features

* add interfaces ([5a36219](https://github.com/jbussdieker/bussdcc/commit/5a362190d1c4974193395bef21ce5dbb820fcb02))

## [0.5.1](https://github.com/jbussdieker/bussdcc/compare/v0.5.0...v0.5.1) (2026-01-30)


### Documentation

* update readme ([3c96893](https://github.com/jbussdieker/bussdcc/commit/3c96893d1b9c25467ee7875dea83f4723f513e87))

## [0.5.0](https://github.com/jbussdieker/bussdcc/compare/v0.4.0...v0.5.0) (2026-01-30)


### Features

* add services ([40984a9](https://github.com/jbussdieker/bussdcc/commit/40984a94ce04c10b11aa17b7226198528e822559))


### Documentation

* update readme ([00340d9](https://github.com/jbussdieker/bussdcc/commit/00340d92e022676780f8bcd853233aec154b7a8c))

## [0.4.0](https://github.com/jbussdieker/bussdcc/compare/v0.3.0...v0.4.0) (2026-01-29)


### Features

* add processes ([4b580e0](https://github.com/jbussdieker/bussdcc/commit/4b580e04da6d3da74f6c39279948183758f7ecf8))
* add state ([bfdfbda](https://github.com/jbussdieker/bussdcc/commit/bfdfbdac3a59d4d6dcfdfe680ae7c5b0723cf051))


### Documentation

* update readme ([3c1d8f6](https://github.com/jbussdieker/bussdcc/commit/3c1d8f6d22a9abc8ac5c7aa3ebcd9845493a62ef))

## [0.3.0](https://github.com/jbussdieker/bussdcc/compare/v0.2.0...v0.3.0) (2026-01-29)


### Features

* add version to runtime ([777d8bd](https://github.com/jbussdieker/bussdcc/commit/777d8bd211a4bb6236d9c7c36100a98f4adbe925))
* improve event system ([281ca16](https://github.com/jbussdieker/bussdcc/commit/281ca161a26b7c1472e358f8f6fb579cfd8bf707))


### Documentation

* update readme ([5e62821](https://github.com/jbussdieker/bussdcc/commit/5e62821bb41bfc38d4625684395ed591a9ab1641))

## [0.2.0](https://github.com/jbussdieker/bussdcc/compare/v0.1.0...v0.2.0) (2026-01-29)


### Features

* add initial runtime ([d4a60cb](https://github.com/jbussdieker/bussdcc/commit/d4a60cb47da2ce0d6b5bca1d1d5b1140b55a096c))

## 0.1.0 (2026-01-29)


### Features

* initial commit ([cb2aaee](https://github.com/jbussdieker/bussdcc/commit/cb2aaeea1e3a2fb0858cd5fdb374577dde8eac6e))
