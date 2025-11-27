from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create sample blog posts for development'
    
    def handle(self, *args, **options):
        # Get or create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@laswostudios.com',
                'first_name': 'John',
                'last_name': 'Laswo'
            }
        )
        
        # Create categories
        categories_data = [
            {'name': 'Home Renovation', 'slug': 'home-renovation', 'description': 'Tips and insights for home renovation projects'},
            {'name': 'Construction Tips', 'slug': 'construction-tips', 'description': 'Professional construction advice and best practices'},
            {'name': 'Design Inspiration', 'slug': 'design-inspiration', 'description': 'Creative design ideas and inspiration for your projects'},
            {'name': 'Industry News', 'slug': 'industry-news', 'description': 'Latest news and trends in the construction industry'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = category
            if created:
                self.stdout.write(f"Created category: {category.name}")
        
        # Create tags
        tags_data = [
            'renovation', 'construction', 'design', 'tips', 'home-improvement',
            'budgeting', 'materials', 'sustainability', 'trends', 'diy', 'industry-news'
        ]
        
        tags = {}
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name.replace('-', ' ').title(),
                slug=tag_name.lower()
            )
            tags[tag_name] = tag
            if created:
                self.stdout.write(f"Created tag: {tag.name}")
        
        # Sample blog posts
        posts_data = [
            {
                'title': '5 Signs Your Home Needs a Renovation',
                'slug': 'signs-home-needs-renovation',
                'category': categories['home-renovation'],
                'excerpt': 'Learn to recognize the key indicators that your home is ready for an upgrade and how to plan your renovation project effectively.',
                'content': """<h2>Is Your Home Trying to Tell You Something?</h2>

<p>As homeowners, we often become accustomed to the little quirks and issues in our living spaces. However, some signs shouldn't be ignored. Recognizing when your home needs renovation can save you money, improve your quality of life, and increase your property's value.</p>

<h3>1. Outdated Electrical Systems</h3>
<p>If you're still relying on two-prong outlets or frequently tripping breakers, your electrical system might be dangerously outdated. Modern homes require more power for today's devices and appliances. Upgrading your electrical system not only improves safety but also accommodates your technology needs.</p>

<h3>2. Persistent Maintenance Issues</h3>
<p>Are you constantly fixing the same problems? Whether it's a leaky roof, drafty windows, or plumbing issues that keep resurfacing, these recurring problems indicate that temporary fixes are no longer sufficient. A comprehensive renovation addresses the root causes.</p>

<h3>3. Changing Family Needs</h3>
<p>Your family's needs evolve over time. What worked when you first moved in might not suit your current lifestyle. Whether you need a home office, more bedrooms, or accessible features for aging family members, renovations can adapt your space to your changing requirements.</p>

<h3>4. Energy Inefficiency</h3>
<p>High utility bills often signal poor insulation, outdated HVAC systems, or inefficient windows. Modern renovation techniques and materials can significantly improve your home's energy efficiency, saving you money while reducing your environmental impact.</p>

<h3>5. Declining Property Value</h3>
<p>If similar homes in your neighborhood are selling for significantly more, your property might need updating. Kitchen and bathroom renovations typically offer the best return on investment, while exterior improvements boost curb appeal.</p>

<h2>Planning Your Renovation</h2>
<p>Once you've identified the need for renovation, proper planning is crucial. Start by:</p>
<ul>
<li>Setting a realistic budget with contingency funds</li>
<li>Researching qualified contractors</li>
<li>Understanding local building codes and permits</li>
<li>Creating a realistic timeline</li>
<li>Considering temporary living arrangements if needed</li>
</ul>

<p>Remember, a well-planned renovation not only improves your immediate living situation but also protects your long-term investment in your home.</p>""",
                'tags': [tags['renovation'], tags['home-improvement'], tags['tips']],
                'is_featured': True,
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': 'Sustainable Building Materials for Modern Construction',
                'slug': 'sustainable-building-materials',
                'category': categories['construction-tips'],
                'excerpt': 'Discover eco-friendly building materials that reduce environmental impact while maintaining quality and durability in construction projects.',
                'content': """<h2>Building a Greener Future</h2>

<p>Sustainability in construction is no longer a trend—it's a necessity. As environmental awareness grows, both homeowners and builders are seeking materials that minimize ecological impact without compromising on quality or aesthetics.</p>

<h3>Bamboo: The Renewable Wonder</h3>
<p>Bamboo has emerged as one of the most versatile sustainable materials. Its rapid growth rate (some species grow up to 3 feet per day) and natural strength make it ideal for flooring, cabinetry, and structural elements. Unlike traditional hardwood trees that take decades to mature, bamboo reaches harvest maturity in just 3-5 years.</p>

<h3>Recycled Steel</h3>
<p>Steel production is energy-intensive, but using recycled steel reduces this impact by up to 75%. Recycled steel maintains the same strength and durability as virgin steel while significantly lowering carbon emissions. It's perfect for structural frames, roofing, and reinforcement.</p>

<h3>Reclaimed Wood</h3>
<p>Reclaimed wood adds character and history to any project while reducing deforestation. Sourced from old barns, factories, and other structures, this material brings unique aesthetics and proven durability. Each piece tells a story while serving practical purposes in flooring, beams, and accent walls.</p>

<h3>Rammed Earth</h3>
<p>This ancient building technique is experiencing a modern revival. Rammed earth walls provide excellent thermal mass, naturally regulating indoor temperatures and reducing energy costs. The material is made from locally sourced soil, minimizing transportation emissions.</p>

<h3>Insulated Concrete Forms (ICFs)</h3>
<p>ICFs combine concrete's durability with superior insulation properties. These interlocking foam blocks create energy-efficient building envelopes that reduce heating and cooling costs by up to 50% compared to traditional construction methods.</p>

<h2>Benefits Beyond Sustainability</h2>
<p>Choosing sustainable materials offers advantages beyond environmental protection:</p>

<ul>
<li><strong>Improved Indoor Air Quality:</strong> Many sustainable materials emit fewer volatile organic compounds (VOCs)</li>
<li><strong>Energy Efficiency:</strong> Better insulation properties reduce utility costs</li>
<li><strong>Durability:</strong> Sustainable materials often outperform conventional alternatives</li>
<li><strong>Health Benefits:</strong> Natural materials can contribute to better occupant health</li>
<li><strong>Increased Property Value:</strong> Green features are increasingly valued in the real estate market</li>
</ul>

<h2>Making the Right Choice</h2>
<p>When selecting sustainable materials, consider:</p>
<ul>
<li>Local availability to reduce transportation impact</li>
<li>Lifecycle assessment of each material</li>
<li>Certifications like FSC for wood or Cradle to Cradle for overall sustainability</li>
<li>Maintenance requirements and longevity</li>
<li>Compatibility with your specific climate and project requirements</li>
</ul>

<p>At Laswo Studios, we're committed to incorporating sustainable practices into every project, helping our clients build beautiful spaces that respect our planet.</p>""",
                'tags': [tags['sustainability'], tags['materials'], tags['construction']],
                'is_featured': True,
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': 'Maximizing Small Spaces: Creative Design Solutions',
                'slug': 'maximizing-small-spaces-design',
                'category': categories['design-inspiration'],
                'excerpt': 'Transform compact areas into functional, beautiful spaces with these innovative design strategies and smart storage solutions.',
                'content': """<h2>Thinking Big in Small Spaces</h2>

<p>Small spaces present unique challenges and opportunities for creative design. With urban living on the rise and the trend toward minimalist lifestyles, maximizing every square foot has never been more important. The key lies in smart planning and innovative solutions that make small spaces feel spacious and functional.</p>

<h3>1. Multi-Functional Furniture</h3>
<p>Invest in furniture that serves multiple purposes. Murphy beds that fold into walls, ottomans with hidden storage, and extendable dining tables can transform a room's functionality throughout the day. Look for pieces that adapt to your changing needs without compromising on style.</p>

<h3>2. Vertical Storage Solutions</h3>
<p>When floor space is limited, look upward. Floor-to-ceiling shelving, hanging pot racks in kitchens, and vertical garden systems utilize often-wasted vertical space. This approach not only provides storage but also draws the eye upward, creating an illusion of height.</p>

<h3>3. Strategic Lighting</h3>
<p>Proper lighting can dramatically affect how spacious a room feels. Layered lighting—combining ambient, task, and accent lights—adds depth and dimension. Consider installing recessed lighting to save space and using mirrors to reflect natural light throughout the room.</p>

<h3>4. Open Floor Plans</h3>
<p>Where structural limitations allow, creating open-concept spaces can make small areas feel significantly larger. Removing non-load-bearing walls between kitchens and living areas creates visual continuity and improves traffic flow.</p>

<h3>5. Smart Color Choices</h3>
<p>Light, neutral colors make spaces feel airy and open, while strategic pops of color can define areas without physical barriers. Consider using the same color palette throughout connected spaces to create visual flow.</p>

<h2>Room-Specific Strategies</h2>

<h3>Small Kitchen Solutions</h3>
<ul>
<li>Install pull-out pantries and corner cabinet organizers</li>
<li>Use magnetic strips for knife storage instead of bulky blocks</li>
<li>Choose appliances with built-in storage capabilities</li>
<li>Implement open shelving for frequently used items</li>
</ul>

<h3>Compact Bathroom Ideas</h3>
<ul>
<li>Use floating vanities to create visual floor space</li>
<li>Install recessed medicine cabinets</li>
<li>Consider pocket doors to save swing space</li>
<li>Use large-format tiles to minimize grout lines and create continuity</li>
</ul>

<h3>Small Bedroom Solutions</h3>
<ul>
<li>Utilize under-bed storage with custom drawers</li>
<li>Install built-in nightstands and shelving</li>
<li>Use mirrors to create depth and reflect light</li>
<li>Consider a platform bed with integrated storage</li>
</ul>

<h2>The Psychology of Small Space Design</h2>
<p>Successful small space design goes beyond physical solutions. It involves understanding how people perceive and experience space. Key psychological principles include:</p>

<ul>
<li><strong>Visual Weight:</strong> Choosing furniture with slender profiles and raised legs</li>
<li><strong>Sight Lines:</strong> Maintaining clear views through spaces</li>
<li><strong>Scale:</strong> Selecting appropriately sized furnishings</li>
<li><strong>Continuity:</strong> Using consistent materials and colors</li>
</ul>

<h2>Professional Insight</h2>
<p>As experienced contractors, we've learned that the most successful small space transformations come from careful planning and custom solutions. Every inch matters, and sometimes the most impactful changes are the subtle ones that improve daily functionality.</p>

<p>Remember: A well-designed small space isn't about having less—it's about making the most of what you have.</p>""",
                'tags': [tags['design'], tags['tips'], tags['home-improvement']],
                'is_featured': False,
                'status': 'published',
                'published_at': timezone.now(),
            },
            {
                'title': '2024 Construction Trends: What Homeowners Need to Know',
                'slug': '2024-construction-trends',
                'category': categories['industry-news'],
                'excerpt': 'Stay ahead of the curve with our overview of the latest construction trends shaping residential building and renovation projects this year.',
                'content': """<h2>The Future of Home Construction is Here</h2>

<p>The construction industry continues to evolve, driven by technological advancements, changing lifestyle needs, and growing environmental consciousness. Understanding these trends can help homeowners make informed decisions about their current and future projects.</p>

<h3>1. Smart Home Integration Becomes Standard</h3>
<p>What was once considered luxury is now becoming standard in new construction and major renovations. Homeowners are expecting integrated smart systems that control lighting, security, climate, and entertainment. The focus has shifted from standalone smart devices to whole-home automation systems that work seamlessly together.</p>

<h3>2. Health and Wellness-Focused Design</h3>
<p>The pandemic has permanently changed how we view our living spaces. Homeowners are prioritizing features that support physical and mental well-being, including:</p>
<ul>
<li>Advanced air purification systems</li>
<li>Natural lighting optimization</li>
<li>Dedicated wellness spaces (meditation rooms, home gyms)</li>
<li>Biophilic design incorporating natural elements</li>
<li>Non-toxic building materials</li>
</ul>

<h3>3. Flexible and Multi-Generational Living</h3>
<p>The rise of remote work and multi-generational households has created demand for adaptable spaces. We're seeing increased interest in:</p>
<ul>
<li>Convertible rooms that serve multiple purposes</li>
<li>In-law suites with separate entrances</li>
<li>Home offices with professional-grade infrastructure</li>
<li>Flex spaces that can evolve with changing family needs</li>
</ul>

<h3>4. Sustainable and Resilient Construction</h3>
<p>Climate change concerns are driving demand for homes that are both environmentally friendly and resilient to extreme weather. Key developments include:</p>
<ul>
<li>Net-zero energy homes</li>
<li>Drought-resistant landscaping</li>
<li>Storm-resistant building techniques</li>
<li>Water conservation systems</li>
<li>Local and recycled materials</li>
</ul>

<h3>5. Outdoor Living Expansion</h3>
<p>Outdoor spaces are being treated as extensions of the interior living area. Homeowners are investing in:</p>
<ul>
<li>Fully equipped outdoor kitchens</li>
<li>Weather-resistant entertainment systems</li>
<li>Permanent structures like pergolas and gazebos</li>
<li>Year-round usability features like outdoor fireplaces and heaters</li>
</ul>

<h2>Technology Transforming Construction</h2>

<h3>Building Information Modeling (BIM)</h3>
<p>BIM technology allows for detailed 3D modeling of projects before construction begins, reducing errors and improving efficiency. Homeowners can virtually walk through their projects and make changes before any physical work starts.</p>

<h3>Prefabricated and Modular Construction</h3>
<p>Once associated with low-quality buildings, prefabrication has evolved into a premium construction method. Factory-built components offer better quality control, faster construction times, and reduced waste.</p>

<h3>3D Printing in Construction</h3>
<p>While still emerging, 3D printing technology is being used to create complex architectural elements and even entire structures. This technology promises to reduce costs and construction time while enabling unique designs.</p>

<h2>What These Trends Mean for Homeowners</h2>

<p>For those planning construction or renovation projects, these trends highlight the importance of:</p>

<ul>
<li><strong>Future-Proofing:</strong> Considering how needs might change in 5-10 years</li>
<li><strong>Technology Infrastructure:</strong> Ensuring homes can support evolving tech needs</li>
<li><strong>Energy Efficiency:</strong> Investing in features that reduce long-term costs</li>
<li><strong>Flexibility:</strong> Designing spaces that can adapt to different uses</li>
<li><strong>Professional Expertise:</strong> Working with contractors who understand these trends</li>
</ul>

<h2>Looking Ahead</h2>
<p>The construction industry's evolution shows no signs of slowing down. As materials science advances and digital tools become more sophisticated, homeowners have more opportunities than ever to create spaces that are beautiful, functional, and forward-thinking.</p>

<p>At Laswo Studios, we stay at the forefront of these developments, ensuring our clients benefit from the latest innovations while maintaining the quality craftsmanship we're known for.</p>""",
                'tags': [tags['trends'], tags['industry-news'], tags['construction']],
                'is_featured': True,
                'status': 'published',
                'published_at': timezone.now(),
            }
        ]
        
        for post_data in posts_data:
            post_tags = post_data.pop('tags')
            post, created = Post.objects.get_or_create(
                slug=post_data['slug'],
                defaults={**post_data, 'author': admin_user}
            )
            
            if created:
                post.tags.set(post_tags)
                self.stdout.write(
                    self.style.SUCCESS(f'Created post: {post.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Post already exists: {post.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample blog posts!')
        )