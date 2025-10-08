"""
Enhanced NLP Chatbot Demo
Demonstrates comprehensive pattern matching with fuel type and luxury detection
"""

import sys
sys.path.insert(0, 'src')
from chatbot import respond_to_user

def print_section(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def demo_query(query, description=""):
    """Test a query and display results"""
    if description:
        print(f"\n📋 {description}")
    print(f"❓ Query: \"{query}\"")
    response = respond_to_user(query)
    print(f"💬 Response: {response}")

# Main Demo
if __name__ == "__main__":
    print("\n" + "🚗"*35)
    print("  AUTOMIND ENHANCED NLP CHATBOT - COMPREHENSIVE DEMO")
    print("🚗"*35)
    
    print_section("1️⃣  SAMPLE QUERIES FROM REQUIREMENTS")
    demo_query(
        "I want a luxury sedan above 40 lakhs",
        "Luxury sedan with price range"
    )
    demo_query(
        "Looking for an electric hatchback by Tesla",
        "Electric vehicle with specific brand"
    )
    demo_query(
        "A cheap Maruti car under 10L",
        "Budget car with brand and price"
    )
    
    print_section("2️⃣  FUEL TYPE EXTRACTION TESTS")
    demo_query(
        "Show me petrol SUVs under 15 lakhs",
        "Petrol fuel type detection"
    )
    demo_query(
        "Budget friendly diesel sedan",
        "Diesel fuel with budget keyword"
    )
    demo_query(
        "Give me EV options under 30 lakhs",
        "EV synonym for electric"
    )
    demo_query(
        "Battery powered cars from Tata",
        "Battery synonym for electric"
    )
    
    print_section("3️⃣  LUXURY/BUDGET DETECTION TESTS")
    demo_query(
        "Premium Hyundai SUV above 20 lakhs",
        "Premium keyword → luxury"
    )
    demo_query(
        "Affordable electric car",
        "Affordable keyword → budget"
    )
    demo_query(
        "High-end BMW sedan",
        "High-end keyword + luxury brand"
    )
    demo_query(
        "Economical hatchback under 8 lakhs",
        "Economical keyword → budget"
    )
    
    print_section("4️⃣  MULTI-ATTRIBUTE QUERIES")
    demo_query(
        "luxury electric sedan above 40 lakhs",
        "All 4 attributes: luxury + fuel + type + price"
    )
    demo_query(
        "budget petrol hatchback from Maruti under 10 lakhs",
        "All 5 attributes: luxury + fuel + type + brand + price"
    )
    demo_query(
        "cheap diesel SUV under 15L",
        "Budget diesel SUV in mid-range"
    )
    
    print_section("5️⃣  SYNONYM VARIATIONS")
    demo_query(
        "Show me crossovers with gasoline",
        "crossover → SUV, gasoline → petrol"
    )
    demo_query(
        "Entry-level saloon cars",
        "entry-level → budget, saloon → sedan"
    )
    demo_query(
        "Flagship hatch models above 10 lacs",
        "flagship → luxury, hatch → hatchback, lacs → price"
    )
    
    print_section("6️⃣  BRAND VARIATIONS")
    demo_query(
        "Maruti Swift under 8 lakhs",
        "Partial brand match: Maruti → Maruti Suzuki"
    )
    demo_query(
        "VW sedan options",
        "VW → Volkswagen (common abbreviation - if added to synonyms)"
    )
    
    print_section("7️⃣  EDGE CASES")
    demo_query(
        "Tata Nexon EV",
        "Model name with EV suffix"
    )
    demo_query(
        "luxury budget car",
        "Conflicting keywords - luxury takes priority"
    )
    demo_query(
        "expensive petrol hatchback under 5 lakhs",
        "Price range suggests budget, but 'expensive' keyword present"
    )
    
    print_section("8️⃣  PARTIAL MATCHES")
    demo_query(
        "Honda models",
        "Only brand specified"
    )
    demo_query(
        "Electric vehicles",
        "Only fuel type specified"
    )
    demo_query(
        "Cars under 20 lakhs",
        "Only price range specified"
    )
    
    print("\n" + "="*70)
    print("  ✅ DEMO COMPLETED - ALL FEATURES DEMONSTRATED")
    print("="*70)
    
    # Summary Statistics
    print("\n📊 ENHANCED NLP CAPABILITIES:")
    print("   • 5 extractable attributes (brand, type, fuel, price, luxury)")
    print("   • 13 brand patterns from dataset")
    print("   • 3 body types with synonym expansion")
    print("   • 3 fuel types with synonym expansion (petrol, diesel, electric)")
    print("   • 4 price bins for Indian market")
    print("   • 7 luxury keywords + 8 budget keywords")
    print("   • Smart context inference (luxury brands, price-based hints)")
    print("   • Generic term filtering (car, vehicle, want, looking, etc.)")
    print("\n")
