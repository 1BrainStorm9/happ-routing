# AbobikPopik routing для Happ

Профиль на основе [RoscomVPN](https://github.com/hydraponique/roscomvpn-routing) с собственными дополнениями. Исходные правила и geo-базы предоставляются авторами RoscomVPN.

## Установка

Откройте [DEFAULT.DEEPLINK](https://raw.githubusercontent.com/1BrainStorm9/happ-routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK), скопируйте весь текст `happ://routing/onadd/...` и импортируйте его в Happ через буфер обмена. Профиль называется **AbobikPopik routing**. При необходимости выберите нужную подписку, затем переподключите VPN.

## Свои сайты

Редактируйте `custom-rules.json`: `ProxySites` — через прокси, `DirectSites` — напрямую, `BlockSites` — блокировать. Для домена вместе с поддоменами используйте `domain:example.com`, для точного имени — `full:example.com`.

GitHub Actions ежедневно и после изменения своих правил получает актуальную исходную маршрутизацию и собирает JSON и deeplink. Свои дополнения сохраняются. Одинаковые записи переносятся в выбранную группу; перекрытия с большими geosite-категориями подчиняются исходному порядку `block-proxy-direct`.

Обновление файлов на GitHub само по себе не обновляет импортированный профиль в Happ. Для применения новой версии импортируйте свежий deeplink с тем же именем и переподключитесь. Автоматическая доставка клиентам через VPN-подписку требует настройки панели отдельно.

## Локальная сборка

Python 3, без сторонних зависимостей: `python build.py`.
