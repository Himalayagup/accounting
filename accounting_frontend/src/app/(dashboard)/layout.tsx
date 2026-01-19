"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { LayoutDashboard, BookOpen, ShoppingCart, Settings, LogOut, Package } from "lucide-react"
import { Button } from "@/components/ui/button"

const sidebarItems = [
    { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { name: "Masters", href: "/masters", icon: BookOpen },
    { name: "Transactions", href: "/transactions", icon: ShoppingCart },
    { name: "Inventory", href: "/inventory", icon: Package },
    { name: "Settings", href: "/settings", icon: Settings },
]

export default function DashboardLayout({
    children,
}: {
    children: React.ReactNode
}) {
    const pathname = usePathname()

    return (
        <div className="flex min-h-screen w-full">
            <div className="hidden border-r bg-gray-100/40 lg:block dark:bg-gray-800/40 w-64">
                <div className="flex h-full max-h-screen flex-col gap-2">
                    <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
                        <Link href="/" className="flex items-center gap-2 font-semibold">
                            <span className="">AccountingEngine</span>
                        </Link>
                    </div>
                    <div className="flex-1">
                        <nav className="grid items-start px-2 text-sm font-medium lg:px-4">
                            {sidebarItems.map((item) => (
                                <Link
                                    key={item.href}
                                    href={item.href}
                                    className={cn(
                                        "flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:text-primary",
                                        pathname.startsWith(item.href)
                                            ? "bg-muted text-primary"
                                            : "text-muted-foreground"
                                    )}
                                >
                                    <item.icon className="h-4 w-4" />
                                    {item.name}
                                </Link>
                            ))}
                        </nav>
                    </div>
                    <div className="mt-auto p-4">
                        <Button variant="outline" className="w-full justify-start gap-2" onClick={() => {
                            localStorage.removeItem('access_token')
                            window.location.href = '/login'
                        }}>
                            <LogOut className="h-4 w-4" />
                            Logout
                        </Button>
                    </div>
                </div>
            </div>
            <div className="flex flex-col w-full">
                <header className="flex h-14 items-center gap-4 border-b bg-gray-100/40 px-6 dark:bg-gray-800/40 lg:h-[60px]">
                    <div className="w-full flex-1">
                        <h1 className="font-semibold text-lg">
                            {sidebarItems.find(i => pathname.startsWith(i.href))?.name || 'Dashboard'}
                        </h1>
                    </div>
                </header>
                <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-6">
                    {children}
                </main>
            </div>
        </div>
    )
}
