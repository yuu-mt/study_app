// Vercelの無料プランでも使えるEdge Middlewareを利用したBasic認証。
// クライアントへのデモ公開時など、一時的にサイト全体へアクセス制限をかけたい場合に使用する。
//
// 有効化するには、Vercelプロジェクトの環境変数に以下を設定してください:
//   DEMO_AUTH_USER, DEMO_AUTH_PASSWORD
// 両方とも未設定の場合は認証をスキップし、通常通り公開されます。
// 不要になったら、この2つの環境変数を削除するだけで認証を解除できます。

export const config = {
  matcher: '/((?!favicon.ico).*)',
}

export default function middleware(request) {
  const user = process.env.DEMO_AUTH_USER
  const pass = process.env.DEMO_AUTH_PASSWORD

  // 環境変数が設定されていなければ認証をスキップ（通常公開）
  if (!user || !pass) {
    return
  }

  const authHeader = request.headers.get('authorization')

  if (authHeader) {
    const [scheme, encoded] = authHeader.split(' ')
    if (scheme === 'Basic' && encoded) {
      const decoded = atob(encoded)
      const separatorIndex = decoded.indexOf(':')
      const inputUser = decoded.substring(0, separatorIndex)
      const inputPass = decoded.substring(separatorIndex + 1)

      if (inputUser === user && inputPass === pass) {
        return
      }
    }
  }

  return new Response('Authentication required', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Monster Study Tracker (Preview)"',
    },
  })
}
